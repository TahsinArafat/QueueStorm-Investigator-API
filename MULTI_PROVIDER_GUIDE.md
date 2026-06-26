# Round-Robin Multi-Provider Configuration Guide

## Overview

The QueueStorm Investigator now supports **multiple AI API endpoints** with automatic **round-robin load balancing** and **failover**. This prevents rate limiting issues during high-traffic periods (e.g., judge evaluation time).

## Features

- ✅ **Round-robin rotation**: Distributes requests evenly across all configured providers
- ✅ **Automatic failover**: If one provider fails (rate limit, timeout), automatically tries the next one
- ✅ **Connection pooling**: OpenAI clients are cached and reused for better performance
- ✅ **Thread-safe**: Safe for concurrent requests in production
- ✅ **Backwards compatible**: Existing single-provider setup continues to work
- ✅ **Smart error handling**: Distinguishes between retriable errors (rate limits, timeouts) and non-retriable errors (auth failures, bad requests)

## Configuration

### Option 1: Multi-Provider Setup (Recommended for Production)

Use the `LLM_PROVIDERS` environment variable with a JSON array:

```bash
# .env
LLM_PROVIDERS='[
  {
    "name": "openai-primary",
    "api_key": "sk-your-key-1",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4o-mini",
    "timeout": 15
  },
  {
    "name": "openai-backup",
    "api_key": "sk-your-key-2",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4o-mini",
    "timeout": 15
  },
  {
    "name": "azure-openai",
    "api_key": "your-azure-key",
    "base_url": "https://your-resource.openai.azure.com",
    "model": "gpt-4o-mini",
    "timeout": 20
  }
]'
```

**Fields:**
- `name` (optional): Provider identifier for logging (defaults to `provider-0`, `provider-1`, etc.)
- `api_key` (required): API authentication key
- `base_url` (optional): API endpoint URL (defaults to `https://api.openai.com/v1`)
- `model` (optional): Model name (defaults to `gpt-4o-mini`)
- `timeout` (optional): Request timeout in seconds (defaults to `15.0`)

### Option 2: Single Provider (Development)

Use the legacy format for simple development setups:

```bash
# .env
OPENAI_API_KEY=sk-your-api-key
OPENAI_API_BASE=https://api.openai.com/v1
MODEL_NAME=gpt-4o-mini
```

**Note:** If `LLM_PROVIDERS` is set, it takes precedence over the legacy variables.

## How It Works

### Round-Robin Rotation

Requests are distributed across providers in order:

```
Request 1 → Provider 1
Request 2 → Provider 2
Request 3 → Provider 3
Request 4 → Provider 1 (cycles back)
Request 5 → Provider 2
...
```

### Automatic Failover

If a provider fails, the system automatically tries the next one:

```
Request → Provider 1 (rate limited) ❌
       → Provider 2 (timeout) ❌
       → Provider 3 (success) ✅
```

### Error Classification

**Retriable errors** (triggers failover):
- Rate limits (HTTP 429)
- Timeouts
- Server errors (HTTP 500, 502, 503)
- Connection failures

**Non-retriable errors** (fails fast to fallback):
- Authentication failures (HTTP 401)
- Bad requests (HTTP 400)
- Model not found (HTTP 404)

If all providers fail, the system falls back to template-based responses (existing behavior).

## Usage Examples

### For Judges (Multiple API Keys)

```bash
# Set up 3 different OpenAI API keys for load distribution
export LLM_PROVIDERS='[
  {"name":"judge-key-1","api_key":"sk-judge-key-1","base_url":"https://api.openai.com/v1","model":"gpt-4o-mini"},
  {"name":"judge-key-2","api_key":"sk-judge-key-2","base_url":"https://api.openai.com/v1","model":"gpt-4o-mini"},
  {"name":"judge-key-3","api_key":"sk-judge-key-3","base_url":"https://api.openai.com/v1","model":"gpt-4o-mini"}
]'

# Start the server
python -m uvicorn app.main:app --port 8000
```

### For Development (Single Key)

```bash
# Simple single-provider setup
export OPENAI_API_KEY=sk-dev-key
export MODEL_NAME=gpt-4o-mini

# Start the server
python -m uvicorn app.main:app --port 8000
```

### Mixed Providers (OpenAI + Azure)

```bash
export LLM_PROVIDERS='[
  {"name":"openai","api_key":"sk-openai-key","base_url":"https://api.openai.com/v1","model":"gpt-4o-mini"},
  {"name":"azure","api_key":"azure-key","base_url":"https://your-resource.openai.azure.com","model":"gpt-4o-mini"}
]'
```

## Monitoring

The system logs provider usage and failures:

```
INFO: Initialized LLM provider pool with 3 providers: ['provider-1', 'provider-2', 'provider-3']
WARNING: Provider 'provider-1' failed (attempt 1/3): RateLimitError: 429 | Retry: True (ticket=TEST-001)
INFO: Provider 'provider-2' succeeded after 1 failures (ticket=TEST-001)
ERROR: All 3 providers exhausted (ticket=TEST-002)
```

## Testing

### Unit Tests

```bash
# Run provider pool tests
pytest tests/test_llm_provider.py -v
```

### Integration Tests

```bash
# Run integration tests
python test_round_robin_integration.py
```

### Manual Testing

```bash
# Make multiple rapid requests to see round-robin in action
for i in {1..10}; do
  curl -X POST http://localhost:8000/analyze-ticket \
    -H "Content-Type: application/json" \
    -d @samples/sample_wrong_transfer_en.json
done
```

Check logs to see which provider handled each request.

## Performance Considerations

- **Connection pooling**: OpenAI clients are cached and reused (not recreated per request)
- **Thread-safe**: Uses threading.Lock for concurrent request safety
- **Minimal overhead**: Round-robin selection is O(1) with simple modulo operation
- **Timeout per provider**: Each provider has independent timeout (default 15s)
  - Total failover time = `num_providers × timeout` (worst case)
  - Example: 3 providers × 15s = 45s maximum before fallback

## Migration Path

1. **Deploy the new code** - no configuration changes needed
2. **Existing deployments continue working** with single provider
3. **Add `LLM_PROVIDERS` when ready** to enable multi-provider support
4. **Start with single provider in JSON format** to validate parsing:
   ```bash
   LLM_PROVIDERS='[{"api_key":"sk-existing-key"}]'
   ```
5. **Add additional providers** as needed

## Troubleshooting

### Issue: "At least one provider required" error

**Cause:** Empty `LLM_PROVIDERS` array or missing `api_key` in all providers

**Fix:** Ensure at least one valid provider with `api_key`:
```bash
LLM_PROVIDERS='[{"api_key":"sk-valid-key"}]'
```

### Issue: JSON parsing error

**Cause:** Invalid JSON syntax in `LLM_PROVIDERS`

**Fix:** Validate JSON syntax. Common issues:
- Missing quotes around strings
- Trailing commas
- Single quotes instead of double quotes (use `'` for outer string, `"` inside JSON)

```bash
# ❌ Wrong (single quotes inside)
LLM_PROVIDERS="[{'api_key':'sk-key'}]"

# ✅ Correct
LLM_PROVIDERS='[{"api_key":"sk-key"}]'
```

### Issue: All providers fail immediately

**Cause:** Non-retriable error (e.g., invalid API key format, bad model name)

**Fix:** Check logs for error details. Common fixes:
- Verify API keys are valid
- Check model names are correct
- Ensure base URLs are accessible

### Issue: Requests still hitting rate limits

**Cause:** Not enough providers configured, or all providers share same rate limit pool

**Fix:** 
- Add more providers with different API keys
- Ensure each API key has separate rate limit quota
- Consider using different API endpoints (OpenAI + Azure)

## Files Changed

- **`app/llm_provider.py`** (new): Provider pool management
- **`app/llm.py`** (modified): Uses provider pool instead of direct OpenAI client
- **`.env.example`** (modified): Documented new configuration format
- **`tests/test_llm_provider.py`** (new): Unit tests for provider pool
- **`test_round_robin_integration.py`** (new): Integration tests

## API Compatibility

**No breaking changes:**
- All API endpoints remain unchanged
- Request/response formats unchanged
- Function signatures unchanged
- Existing single-provider deployments continue working

The multi-provider feature is a drop-in enhancement that preserves full backwards compatibility.
