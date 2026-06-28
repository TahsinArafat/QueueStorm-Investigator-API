# Round-Robin Multi-Provider Implementation

## Overview

Technical documentation for the round-robin multi-provider LLM system.

Date: 2026-06-26
Status: Complete and tested

## Architecture

```
FastAPI App (app/main.py)
    ↓
LLM Text Generation (app/llm.py)
    ↓
Provider Pool (app/llm_provider.py)
    ├── Provider 1
    ├── Provider 2
    └── Provider 3
    ↓ (all fail)
Fallback Templates
```

## Round-Robin Algorithm

Uses atomic counter with modulo arithmetic:

```python
class LLMProviderPool:
    def __init__(self, providers):
        self._providers = providers
        self._counter = 0
        self._lock = threading.Lock()
    
    def get_next_provider(self):
        with self._lock:
            index = self._counter % len(self._providers)
            self._counter += 1
        config = self._providers[index]
        return config.name, self._get_client(config), config
```

With 3 providers, requests cycle: p1 → p2 → p3 → p1 → ...

Properties:
- Fair distribution (±1 request per provider)
- O(1) complexity
- Thread-safe via threading.Lock

## Failover

Retriable errors (try next provider):
- Rate limits (429)
- Timeouts
- Server errors (500, 502, 503)
- Connection failures

Non-retriable errors (fail fast):
- Auth failures (401)
- Bad requests (400)
- Model not found (404)

## Connection Pooling

OpenAI clients are cached and reused:

```python
if config.name not in self._clients:
    with self._lock:
        if config.name not in self._clients:
            self._clients[config.name] = OpenAI(...)
```

## Configuration

Single provider (legacy):
```bash
OPENAI_API_KEY=sk-your-api-key
MODEL_NAME=gpt-4o-mini
```

Multiple providers:
```bash
LLM_PROVIDERS='[
  {"name":"openai-1","api_key":"sk-key-1","base_url":"https://api.openai.com/v1","model":"gpt-4o-mini","timeout":15},
  {"name":"azure","api_key":"azure-key","base_url":"https://your-resource.openai.azure.com","model":"gpt-4o-mini","timeout":20}
]'
```

Priority: LLM_PROVIDERS > OPENAI_API_KEY > empty list

## Thread Safety

Counter increment: ~1μs (minimal lock hold)
Client creation: ~1-5ms (rare, only first access)
API calls: Not locked (may take seconds)

## Testing

Unit tests: 27 tests in `tests/test_llm_provider.py`
Integration tests: `test_round_robin_integration.py`

```bash
pytest tests/test_llm_provider.py -v
pytest tests/ -v
```

## Performance

| Operation | Complexity |
|-----------|------------|
| Get next provider | O(1) |
| Client creation | O(1) cached |
| Failover attempt | O(N) |
| Error classification | O(M) |

Overhead per request: ~2μs
Total clients: N (one per provider)

## Monitoring

Log messages:
```
INFO: Initialized LLM provider pool with 3 providers
WARNING: Provider 'provider-1' failed: RateLimitError: 429
INFO: Provider 'provider-2' succeeded after 1 failures
ERROR: All 3 providers exhausted
```

## Troubleshooting

Uneven distribution: Restart to reset counter.

High fallback rate: Check logs for error patterns (429 = rate limit, 401 = invalid key, timeout = network).

JSON parsing error:
```bash
# Wrong
LLM_PROVIDERS="[{'api_key':'sk-key'}]"

# Correct
LLM_PROVIDERS='[{"api_key":"sk-key"}]'
```

## Migration

From single to multi-provider:

Step 1: Convert to JSON format
```bash
LLM_PROVIDERS='[{"api_key":"sk-current-key","model":"gpt-4o-mini"}]'
```

Step 2: Add second provider
```bash
LLM_PROVIDERS='[
  {"name":"primary","api_key":"sk-current-key","model":"gpt-4o-mini"},
  {"name":"backup","api_key":"sk-new-key","model":"gpt-4o-mini"}
]'
```

Rollback: Remove LLM_PROVIDERS and restart.

## Security

- API keys stored in environment variables
- Keys masked in logs
- Keys not included in error messages
- .env in .gitignore

## Future Enhancements

- Weighted round-robin
- Health checks
- Circuit breaker
- Adaptive timeout
- Metrics dashboard
