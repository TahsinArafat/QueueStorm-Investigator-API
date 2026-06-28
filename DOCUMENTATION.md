# QueueStorm Investigator - Complete Documentation

**Version:** 1.0.0  
**Repository:** https://github.com/TahsinArafat/QueueStorm-Investigator-API  
**Status:** Production Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [API Reference](#api-reference)
5. [Installation & Deployment](#installation--deployment)
6. [Configuration](#configuration)
7. [Testing](#testing)
8. [Performance](#performance)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)

---

## Overview

QueueStorm Investigator is an AI-powered customer support ticket analysis system designed for digital financial services platforms in Bangladesh. It automatically analyzes complaint tickets, classifies issues, matches transaction evidence, and generates multilingual responses in English, Bangla, and Banglish.

### Key Capabilities

- **Multilingual Support**: English, Bangla (Unicode), Banglish (Romanized)
- **AI-Powered Analysis**: Hybrid language detection and LLM-based text generation
- **Transaction Evidence Matching**: Automatic matching with transaction history
- **Case Classification**: 8 predefined case types with smart routing
- **Safety Compliance**: Automatic credential scrubbing and policy enforcement
- **High Performance**: <5s response time with round-robin load balancing

---

## Features

### 1. AI Language Detection

**Hybrid Detection System:**
- **Rule-based (Fast Path)**: Handles 80% of cases in <1ms
- **AI-powered (Accuracy Path)**: For ambiguous cases requiring context
- **Automatic Fallback**: Graceful degradation if AI unavailable

**Supported Languages:**
- English: "I sent 5000 taka to wrong number"
- Bangla: "আমি ভুল নম্বরে টাকা পাঠিয়েছি"
- Banglish: "Ami vul number e taka pathaise"

**Implementation:** `app/language_detector.py`

### 2. Round-Robin Load Balancing

**Features:**
- Multiple LLM provider support (2+ providers)
- Thread-safe counter-based rotation
- Automatic failover if provider fails
- Double-checked locking for singleton safety

**Configuration:**
```json
LLM_PROVIDERS='[
  {"name":"provider-1","api_key":"KEY1","base_url":"https://api.groq.com/openai/v1","model":"openai/gpt-oss-120b","timeout":15},
  {"name":"provider-2","api_key":"KEY2","base_url":"https://api.groq.com/openai/v1","model":"openai/gpt-oss-120b","timeout":15}
]'
```

**Implementation:** `app/llm_provider.py`

### 3. Case Classification

**8 Case Types:**
1. `wrong_transfer` - Money sent to incorrect recipient
2. `payment_failed` - Payment attempt failed
3. `refund_request` - Customer requesting refund
4. `duplicate_payment` - Multiple charges for same transaction
5. `merchant_settlement_delay` - Merchant payment not received
6. `agent_cash_in_issue` - Agent transaction problems
7. `phishing_or_social_engineering` - Security threats
8. `other` - Unclassified issues

**Implementation:** `app/rules.py`

### 4. Evidence Verdict System

**Three Verdict Types:**
- `consistent` - Transaction evidence supports complaint
- `inconsistent` - Transaction contradicts complaint
- `insufficient_data` - Not enough evidence to determine

**Logic:**
- Matches transactions by amount, type, counterparty
- Compares claim vs actual transaction status
- Detects contradictions and missing data

### 5. Safety Compliance

**Automatic Enforcement:**
- PIN/OTP leak detection and scrubbing
- Refund policy verbiage enforcement
- Security warnings in all languages
- Unicode normalization for special characters

**Example Safety Text:**
- English: "Please do not share your PIN or OTP with anyone."
- Bangla: "অনুগ্রহ করে আপনার পিন (PIN) বা ওটিপি (OTP) কারো সাথে শেয়ার করবেন না।"
- Banglish: Similar to Bangla (uses Bengali script)

**Implementation:** `app/safety.py`

---

## Architecture

### System Flow

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

### Components

**Core Modules:**
- `app/main.py` - FastAPI application and endpoints
- `app/rules.py` - Business logic and classification
- `app/llm.py` - LLM integration and fallback templates
- `app/llm_provider.py` - Round-robin provider pool
- `app/language_detector.py` - AI language detection
- `app/safety.py` - Safety compliance enforcement
- `app/schemas.py` - Pydantic data models

**Testing:**
- `tests/` - Unit tests (37 tests, 100% passing)
- `test_cases/` - Integration test cases
- `tests/conftest.py` - Global fixtures (auto-mocks LLM)

---

## API Reference

### Base URL

```
Production: http://YOUR_VPS_IP:8000
Local: http://localhost:8000
```

### Endpoints

#### 1. Health Check

**GET** `/health`

Check API health status.

**Response:**
```json
{
  "status": "ok"
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

---

#### 2. Analyze Ticket

**POST** `/analyze-ticket`

Analyze a customer support ticket with AI.

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ticket_id` | string | Yes | Unique ticket identifier |
| `complaint` | string | Yes | Customer complaint text |
| `language` | string | No | Language code (en/bn/mixed). Auto-detected if not provided |
| `channel` | string | No | Communication channel |
| `user_type` | string | No | User type (customer/merchant/agent) |
| `transaction_history` | array | No | Array of transaction objects |

**Transaction Object:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `transaction_id` | string | Yes | Unique transaction ID |
| `timestamp` | string | Yes | ISO 8601 timestamp |
| `type` | string | Yes | transfer/payment/cash_in/cash_out/settlement/refund |
| `amount` | number | Yes | Transaction amount |
| `counterparty` | string | Yes | Phone number or merchant ID |
| `status` | string | Yes | completed/failed/pending/reversed |

**Response:**

```json
{
  "ticket_id": "TEST-001",
  "relevant_transaction_id": "TXN-12345",
  "evidence_verdict": "consistent",
  "case_type": "wrong_transfer",
  "severity": "high",
  "department": "dispute_resolution",
  "agent_summary": "Customer sent 5000 Taka to an incorrect phone number...",
  "recommended_next_action": "Create a wrong-transfer dispute case...",
  "customer_reply": "Thank you for contacting us. I understand...",
  "human_review_required": true,
  "confidence": 0.9,
  "reason_codes": ["wrong_transfer", "consistent"]
}
```

**Example Request:**

```bash
curl -X POST http://localhost:8000/analyze-ticket \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "TEST-001",
    "complaint": "I sent 5000 taka to wrong number +8801712345678",
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
  }'
```

**Response Codes:**
- `200 OK` - Successful analysis
- `422 Unprocessable Entity` - Invalid request body
- `500 Internal Server Error` - Server error

---

## Installation & Deployment

### Prerequisites

- Python 3.9+
- pip
- Virtual environment (recommended)
- Groq API key (or compatible OpenAI API)

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/TahsinArafat/QueueStorm-Investigator-API.git
cd SUST_Hackathon_2026_Preli

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 5. Run tests
pytest tests/ -v

# 6. Start development server
uvicorn app.main:app --reload --port 8000
```

### VPS Production Deployment

**Quick Deploy (Python Only):**

```bash
# 1. Clone and setup
git clone https://github.com/TahsinArafat/QueueStorm-Investigator-API.git
cd SUST_Hackathon_2026_Preli
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
nano .env  # Add your LLM_PROVIDERS

# 3. Open firewall
sudo ufw allow 8000/tcp
sudo ufw allow 22/tcp
sudo ufw enable

# 4. Start server (background)
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &

# 5. Verify
curl http://localhost:8000/health
```

**Production with Systemd (Recommended):**

```bash
# Create service file
sudo nano /etc/systemd/system/queuestorm.service
```

```ini
[Unit]
Description=QueueStorm Investigator API
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/SUST_Hackathon_2026_Preli
Environment="PATH=/path/to/SUST_Hackathon_2026_Preli/.venv/bin"
ExecStart=/path/to/SUST_Hackathon_2026_Preli/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable queuestorm
sudo systemctl start queuestorm
sudo systemctl status queuestorm
```

**Docker Deployment:**

```bash
# Build image
docker build -t queuestorm .

# Run container
docker run -d \
  --name queuestorm \
  -p 8000:8000 \
  --env-file .env \
  queuestorm
```

---

## Configuration

### Environment Variables

**Required:**

```bash
LLM_PROVIDERS='[{"name":"provider-1","api_key":"YOUR_API_KEY","base_url":"https://api.groq.com/openai/v1","model":"openai/gpt-oss-120b","timeout":15}]'
```

**LLM Provider Configuration:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Provider identifier |
| `api_key` | string | Yes | API authentication key |
| `base_url` | string | Yes | API endpoint URL |
| `model` | string | Yes | Model name/identifier |
| `timeout` | number | Yes | Request timeout in seconds |

**Example (Multiple Providers for Round-Robin):**

```bash
LLM_PROVIDERS='[
  {
    "name":"groq-1",
    "api_key":"gsk_...",
    "base_url":"https://api.groq.com/openai/v1",
    "model":"openai/gpt-oss-120b",
    "timeout":15
  },
  {
    "name":"groq-2",
    "api_key":"gsk_...",
    "base_url":"https://api.groq.com/openai/v1",
    "model":"openai/gpt-oss-120b",
    "timeout":15
  }
]'
```

---

## Testing

### Unit Tests

```bash
# Run all unit tests
pytest tests/ -v

# Run specific test file
pytest tests/test_rules.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

**Expected Output:**
```
37 passed in 0.23s
```

### Integration Tests

```bash
# Run integration tests with real API
python3 test_via_api.py

# Test specific sample cases
curl -X POST http://localhost:8000/analyze-ticket \
  -H "Content-Type: application/json" \
  -d @test_cases/sample_case.json
```

### Interactive Testing

Visit the web interface:
```
http://YOUR_VPS_IP:8000/
```

Features:
- Health check testing
- Pre-loaded examples (English, Bangla, Banglish)
- Live API testing with response display
- JSON request/response formatting

---

## Performance

### Benchmarks

**Unit Tests:**
- Execution Time: 0.23s
- Coverage: All core modules
- Pass Rate: 100% (37/37)

**Integration Tests (Official Samples):**
- Pass Rate: 100% (10/10)
- Average Latency: 1.55s
- Latency Range: 1.10s - 1.96s
- Under 5s Target: 100%

**Load Testing:**
```bash
# Test 100 requests, 10 concurrent
ab -n 100 -c 10 -p payload.json -T application/json http://localhost:8000/analyze-ticket
```

**Expected Throughput:**
- Single Worker: ~10-20 req/sec
- 4 Workers: ~40-80 req/sec

### Optimization Tips

1. **Use Multiple Workers:**
```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

2. **Enable Caching (Optional):**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def detect_language_cached(text: str) -> str:
    return detect_language(text).value
```

3. **Use Multiple LLM Providers:**
Configure 2+ providers for automatic load balancing

---

## Troubleshooting

### Common Issues

**Issue: "No module named 'app'"**
```bash
# Solution: Set PYTHONPATH
export PYTHONPATH=/path/to/SUST_Hackathon_2026_Preli:$PYTHONPATH
```

**Issue: "No LLM provider configuration found"**
```bash
# Solution: Check .env file
cat .env | grep LLM_PROVIDERS

# Test loading
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('LLM_PROVIDERS'))"
```

**Issue: Port 8000 already in use**
```bash
# Solution: Kill existing process
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --port 8080
```

**Issue: Slow response times**
- Check LLM provider latency
- Increase timeout in configuration
- Add more providers for load balancing
- Check system resources (CPU, memory)

**Issue: Tests failing with import errors**
```bash
# Solution: Install in editable mode
pip install -e .

# Or set PYTHONPATH before running
PYTHONPATH=. pytest tests/ -v
```

### Logging

**View Logs (systemd):**
```bash
sudo journalctl -u queuestorm -f
```

**View Logs (nohup):**
```bash
tail -f server.log
```

**Enable Debug Logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Run tests: `pytest tests/ -v`
5. Check linting: `flake8 app/`
6. Commit with descriptive message
7. Push and create pull request

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings for functions
- Keep functions under 50 lines
- Write tests for new features

### Testing Guidelines

- Write unit tests for all new functions
- Ensure 100% pass rate before pushing
- Add integration tests for new endpoints
- Mock external API calls in tests

---

## License

Copyright (c) 2026 QueueStorm Investigator Team  
All rights reserved.

---

## Support

**Repository:** https://github.com/TahsinArafat/QueueStorm-Investigator-API  
**Issues:** https://github.com/TahsinArafat/QueueStorm-Investigator-API/issues  

For deployment questions, refer to the troubleshooting section or check existing issues.

---

**Last Updated:** 2026-06-26  
**Version:** 1.0.0  
**Status:** Production Ready

