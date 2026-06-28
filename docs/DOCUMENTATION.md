# QueueStorm Investigator - Documentation

## Overview

Customer support ticket analysis system for digital financial services in Bangladesh. Analyzes complaint tickets, classifies issues, matches transaction evidence, and generates multilingual responses.

## Features

### Language Detection

Hybrid system with rule-based fast path and AI fallback:

- English: "I sent 5000 taka to wrong number"
- Bangla: "আমি ভুল নম্বরে টাকা পাঠিয়েছি"
- Banglish: "Ami vul number e taka pathaise"

Rules handle 80% of cases in <1ms. AI handles ambiguous cases.

### Round-Robin Load Balancing

Multiple LLM providers with automatic rotation and failover. Thread-safe counter-based distribution.

```json
LLM_PROVIDERS='[
  {"name":"provider-1","api_key":"KEY1","base_url":"https://api.groq.com/openai/v1","model":"openai/gpt-oss-120b","timeout":15},
  {"name":"provider-2","api_key":"KEY2","base_url":"https://api.groq.com/openai/v1","model":"openai/gpt-oss-120b","timeout":15}
]'
```

### Case Classification

8 case types: wrong_transfer, payment_failed, refund_request, duplicate_payment, merchant_settlement_delay, agent_cash_in_issue, phishing_or_social_engineering, other.

### Evidence Verdict

- consistent: Transaction supports complaint
- inconsistent: Transaction contradicts complaint
- insufficient_data: Not enough evidence

### Safety Compliance

PIN/OTP scrubbing, security warnings, refund policy enforcement, Unicode normalization.

## Architecture

```
Client Request
    ↓
FastAPI Endpoint (/analyze-ticket)
    ↓
Language Detection (Hybrid: Rules + AI)
    ↓
Transaction Matching (Evidence Analysis)
    ↓
Case Classification (8 Case Types)
    ↓
LLM Text Generation (Round-Robin)
    ↓
Safety Guard (Compliance Enforcement)
    ↓
Response (JSON with metadata + text)
```

## API

### GET /health

Returns `{"status": "ok"}`

### POST /analyze-ticket

Request body:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ticket_id | string | Yes | Unique ticket identifier |
| complaint | string | Yes | Customer complaint text |
| language | string | No | Language code (en/bn/mixed). Auto-detected if not provided |
| transaction_history | array | No | Array of transaction objects |

Transaction object:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| transaction_id | string | Yes | Unique transaction ID |
| timestamp | string | Yes | ISO 8601 timestamp |
| type | string | Yes | transfer/payment/cash_in/cash_out/settlement/refund |
| amount | number | Yes | Transaction amount |
| counterparty | string | Yes | Phone number or merchant ID |
| status | string | Yes | completed/failed/pending/reversed |

Response:

```json
{
  "ticket_id": "TEST-001",
  "relevant_transaction_id": "TXN-12345",
  "evidence_verdict": "consistent",
  "case_type": "wrong_transfer",
  "severity": "high",
  "department": "dispute_resolution",
  "agent_summary": "Customer sent 5000 Taka to an incorrect phone number...",
  "customer_reply": "Thank you for contacting us...",
  "human_review_required": true,
  "confidence": 0.9
}
```

## Installation

### Local Development

```bash
git clone https://github.com/TahsinArafat/QueueStorm-Investigator-API.git
cd QueueStorm-Investigator-API
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
pytest tests/ -v
uvicorn app.main:app --reload --port 8000
```

### VPS Deployment

```bash
git clone https://github.com/TahsinArafat/QueueStorm-Investigator-API.git
cd QueueStorm-Investigator-API
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
```

### Systemd Service

```ini
[Unit]
Description=QueueStorm Investigator API
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/QueueStorm-Investigator-API
Environment="PATH=/path/to/QueueStorm-Investigator-API/.venv/bin"
ExecStart=/path/to/QueueStorm-Investigator-API/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### Docker

```bash
docker build -t queuestorm .
docker run -d --name queuestorm -p 8000:8000 --env-file .env queuestorm
```

## Configuration

Required environment variable:

```bash
LLM_PROVIDERS='[{"name":"provider-1","api_key":"YOUR_API_KEY","base_url":"https://api.groq.com/openai/v1","model":"openai/gpt-oss-120b","timeout":15}]'
```

Provider fields:

| Field | Type | Description |
|-------|------|-------------|
| name | string | Provider identifier |
| api_key | string | API authentication key |
| base_url | string | API endpoint URL |
| model | string | Model name/identifier |
| timeout | number | Request timeout in seconds |

## Testing

```bash
# Unit tests
pytest tests/ -v
# 37 passed in 0.23s

# With coverage
pytest tests/ --cov=app --cov-report=html

# Integration tests
python3 test_via_api.py
```

## Performance

- Unit tests: 37/37 passing in 0.23s
- Integration tests: 10/10 passing
- Average latency: 1.55s
- Throughput: 10-20 req/sec (single worker)

Production optimization:

```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## Troubleshooting

**No module named 'app':**
```bash
export PYTHONPATH=/path/to/QueueStorm-Investigator-API:$PYTHONPATH
```

**No LLM provider configuration found:**
```bash
cat .env | grep LLM_PROVIDERS
```

**Port 8000 already in use:**
```bash
lsof -ti:8000 | xargs kill -9
```

**View logs:**
```bash
tail -f server.log
# or
sudo journalctl -u queuestorm -f
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Run tests: `pytest tests/ -v`
5. Commit and push
6. Create pull request

## License

Copyright (c) 2026 QueueStorm Investigator Team. All rights reserved.
