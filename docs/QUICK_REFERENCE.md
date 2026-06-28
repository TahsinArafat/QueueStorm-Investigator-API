# Round-Robin Multi-Provider: Quick Reference

## Setup

Add multiple API keys to `.env`:

```bash
LLM_PROVIDERS='[{"api_key":"sk-key-1"},{"api_key":"sk-key-2"},{"api_key":"sk-key-3"}]'
```

Restart app. Done.

## How It Works

```
Request 1 → Provider 1
Request 2 → Provider 2
Request 3 → Provider 3
Request 4 → Provider 1 (cycles back)
```

If a provider fails, the next one is tried automatically. If all fail, template fallback kicks in.

## Configuration

| Field | Required | Default | Example |
|-------|----------|---------|---------|
| api_key | Yes | - | "sk-abc123" |
| name | No | "provider-0" | "openai-primary" |
| base_url | No | "https://api.openai.com/v1" | - |
| model | No | "gpt-4o-mini" | - |
| timeout | No | 15 | 20 |

## Commands

```bash
# Check providers loaded
python -c "from app.llm_provider import get_provider_pool; pool = get_provider_pool(); print(f'Loaded {len(pool._providers)} providers')"

# Run tests
pytest tests/test_llm_provider.py -v

# Start app
python -m uvicorn app.main:app --port 8000
```

## Troubleshooting

JSON parse error:
```bash
# Wrong
LLM_PROVIDERS="[{'api_key':'sk-key'}]"

# Correct
LLM_PROVIDERS='[{"api_key":"sk-key"}]'
```

Rate limits: Add more providers.

All providers fail: Check API keys, model names, and base URLs.

## Error Types

Retriable (auto-failover): timeout, 429, 500/502/503, connection errors

Non-retriable (fast-fail): 401, 400, 404

## Performance

- Overhead per request: ~2μs
- Lock contention: <1ms under high load
- Client creation: Once per provider (cached)
