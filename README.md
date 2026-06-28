# QueueStorm Investigator

Customer support ticket analysis system for digital financial services in Bangladesh.

## Overview

Analyzes complaint tickets automatically: detects language (English, Bangla, Banglish), classifies issues, matches transaction evidence, and generates responses.

## Quick Start

```bash
git clone https://github.com/TahsinArafat/QueueStorm-Investigator-API.git
cd QueueStorm-Investigator-API
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your LLM_PROVIDERS
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
```

Access at `http://YOUR_IP:8000`

## Features

- Language detection (English, Bangla, Banglish)
- Round-robin load balancing across multiple LLM providers
- Transaction evidence matching
- Case classification (8 types)
- PIN/OTP scrubbing and safety compliance

## API

### GET /health

Returns `{"status": "ok"}`

### POST /analyze-ticket

Request:
```json
{
  "ticket_id": "TEST-001",
  "complaint": "I sent 5000 taka to wrong number",
  "transaction_history": [
    {
      "transaction_id": "TXN-12345",
      "timestamp": "2026-04-14T14:10:00Z",
      "type": "transfer",
      "amount": 5000,
      "counterparty": "+8801712345678",
      "status": "completed"
    }
  ]
}
```

Response:
```json
{
  "ticket_id": "TEST-001",
  "case_type": "wrong_transfer",
  "evidence_verdict": "consistent",
  "department": "dispute_resolution",
  "agent_summary": "Customer sent 5000 Taka to incorrect recipient...",
  "customer_reply": "Thank you for contacting us...",
  "human_review_required": true,
  "confidence": 0.9
}
```

## Testing

```bash
pytest tests/ -v
# 37 passed in 0.23s
```

## Configuration

Create `.env` file with your LLM provider:

```bash
LLM_PROVIDERS='[
  {
    "name":"provider-1",
    "api_key":"YOUR_GROQ_API_KEY",
    "base_url":"https://api.groq.com/openai/v1",
    "model":"openai/gpt-oss-120b",
    "timeout":15
  }
]'
```

Add multiple providers for automatic load balancing.

## Project Structure

```
app/
├── main.py                 # FastAPI application
├── llm.py                  # LLM integration
├── llm_provider.py         # Round-robin pool
├── language_detector.py    # Language detection
├── rules.py                # Business logic
├── safety.py               # Safety compliance
├── schemas.py              # Data models
└── static/
    └── index.html          # Web interface
tests/                      # Unit tests
test_cases/                 # Integration tests
```

## Management

```bash
# Start (foreground)
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Start (background)
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &

# Stop
lsof -ti:8000 | xargs kill -9

# Logs
tail -f server.log
```

## Troubleshooting

**Port in use:** `lsof -ti:8000 | xargs kill -9`

**Import errors:** `export PYTHONPATH=$(pwd):$PYTHONPATH`

## License

Copyright (c) 2026 QueueStorm Investigator Team. All rights reserved.
