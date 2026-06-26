# Round-Robin Multi-Provider: Quick Reference

## TL;DR

Add multiple API keys to avoid rate limits during judge time:

```bash
# In .env file:
LLM_PROVIDERS='[{"api_key":"sk-key-1"},{"api_key":"sk-key-2"},{"api_key":"sk-key-3"}]'
```

Restart app. Done. 🎉

---

## Common Scenarios

### Development (1 API Key)

```bash
# .env
OPENAI_API_KEY=sk-your-dev-key
MODEL_NAME=gpt-4o-mini
```

### Judge Time (3 API Keys for 3x Capacity)

```bash
# .env
LLM_PROVIDERS='[
  {"name":"key-1","api_key":"sk-judge-key-1","model":"gpt-4o-mini"},
  {"name":"key-2","api_key":"sk-judge-key-2","model":"gpt-4o-mini"},
  {"name":"key-3","api_key":"sk-judge-key-3","model":"gpt-4o-mini"}
]'
```

### Mixed Providers (OpenAI + Azure)

```bash
LLM_PROVIDERS='[
  {"name":"openai","api_key":"sk-openai-key","base_url":"https://api.openai.com/v1","model":"gpt-4o-mini"},
  {"name":"azure","api_key":"azure-key","base_url":"https://your-resource.openai.azure.com","model":"gpt-4o-mini"}
]'
```

---

## How It Works

```
Request 1 → Provider 1
Request 2 → Provider 2
Request 3 → Provider 3
Request 4 → Provider 1 (cycles back)
Request 5 → Provider 2
...
```

**If Provider 1 fails:**
```
Request → Provider 1 ❌ (rate limit)
       → Provider 2 ✅ (success)
```

**If ALL fail:**
```
Request → Provider 1 ❌
       → Provider 2 ❌
       → Provider 3 ❌
       → Template fallback ✅ (always works)
```

---

## Configuration Fields

| Field | Required | Default | Example |
|-------|----------|---------|---------|
| `api_key` | ✅ Yes | - | `"sk-abc123"` |
| `name` | No | `"provider-0"` | `"openai-primary"` |
| `base_url` | No | `"https://api.openai.com/v1"` | `"https://api.openai.com/v1"` |
| `model` | No | `"gpt-4o-mini"` | `"gpt-4o-mini"` |
| `timeout` | No | `15` | `20` |

---

## Commands

### Test Configuration

```bash
# Check if providers load correctly
python -c "from app.llm_provider import get_provider_pool; pool = get_provider_pool(); print(f'✓ Loaded {len(pool._providers)} provider(s)')"
```

### Run Tests

```bash
# Unit tests
pytest tests/test_llm_provider.py -v

# Integration tests
python test_round_robin_integration.py

# Full suite
pytest tests/ -v
```

### Start Application

```bash
# Standard
python -m uvicorn app.main:app --port 8000

# With reload (development)
python -m uvicorn app.main:app --port 8000 --reload
```

### Monitor Logs

```bash
# Watch for provider rotation
tail -f /var/log/app.log | grep "Provider"

# Count failures by provider
grep "failed" /var/log/app.log | cut -d"'" -f2 | sort | uniq -c
```

---

## Troubleshooting

### JSON Parse Error

```bash
# ❌ Wrong
LLM_PROVIDERS="[{'api_key':'sk-key'}]"

# ✅ Correct
LLM_PROVIDERS='[{"api_key":"sk-key"}]'
```

### Still Getting Rate Limits

**Solution:** Add more providers or verify each has separate rate limit quota.

### All Providers Fail

**Check:**
1. Are API keys valid? (test individually)
2. Are model names correct?
3. Are base URLs accessible?

**Quick test:**
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Templates Used Instead of LLM

**This is normal when:**
- No API keys configured (fallback by design)
- All providers hit rate limits
- Network issues

**Check logs for:**
- `"All N providers exhausted"` → Add more providers
- `"401"` → Invalid API key
- `"timeout"` → Network issue

---

## Performance

| Metric | Value |
|--------|-------|
| **Overhead per request** | ~2μs (negligible) |
| **Lock contention** | <1ms under high load |
| **Client creation** | Once per provider (cached) |
| **Failover time** | providers × timeout (max 15s × N) |

---

## Examples

### Add 2nd Provider to Existing Setup

**Before:**
```bash
OPENAI_API_KEY=sk-current-key
```

**After:**
```bash
LLM_PROVIDERS='[
  {"api_key":"sk-current-key"},
  {"api_key":"sk-new-key"}
]'
```

### Different Models per Provider

```bash
LLM_PROVIDERS='[
  {"name":"fast","api_key":"sk-1","model":"gpt-4o-mini"},
  {"name":"powerful","api_key":"sk-2","model":"gpt-4o"}
]'
```

### Different Timeouts

```bash
LLM_PROVIDERS='[
  {"name":"fast-provider","api_key":"sk-1","timeout":10},
  {"name":"slow-provider","api_key":"sk-2","timeout":30}
]'
```

---

## Error Types

### Retriable (Auto-Failover)
- ⏱️ `timeout` → Try next
- 🚫 `429` rate limit → Try next
- 🔧 `500`/`502`/`503` server error → Try next
- 🔌 `connection` error → Try next

### Non-Retriable (Fast-Fail)
- 🔑 `401` auth failure → Skip to fallback
- ❌ `400` bad request → Skip to fallback
- 🔍 `404` model not found → Skip to fallback

---

## Files Changed

| File | Status | Purpose |
|------|--------|---------|
| `app/llm_provider.py` | NEW | Provider pool logic |
| `app/llm.py` | MODIFIED | Uses provider pool |
| `.env` | MODIFIED | Added multi-provider example |
| `.env.example` | MODIFIED | Documented formats |
| `tests/test_llm_provider.py` | NEW | 27 unit tests |
| `test_round_robin_integration.py` | NEW | Integration tests |

---

## Links

- **Full Guide:** [MULTI_PROVIDER_GUIDE.md](../MULTI_PROVIDER_GUIDE.md)
- **Technical Docs:** [ROUND_ROBIN_IMPLEMENTATION.md](ROUND_ROBIN_IMPLEMENTATION.md)
- **Changelog:** [CHANGELOG_ROUND_ROBIN.md](CHANGELOG_ROUND_ROBIN.md)

---

## Support

**Need help?**
1. Check logs: `grep "Provider" /var/log/app.log`
2. Run tests: `pytest tests/test_llm_provider.py -v`
3. Verify config: `echo $LLM_PROVIDERS | jq`
4. See troubleshooting in full docs

**Common fixes:**
- Invalid JSON → Check quotes
- Rate limits → Add more providers
- Auth errors → Verify API keys
- All fail → Check internet/firewall

---

**Version:** 1.0.0  
**Last Updated:** 2026-06-26
