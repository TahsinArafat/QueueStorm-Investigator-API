# QueueStorm Investigator

An AI-powered support ticket analysis and routing API copilot for digital finance systems. It reads user complaints (supporting English, Bangla, and Banglish), cross-references them against transaction history logs to resolve evidence consistency, categorizes the case, routes it to the appropriate department, drafts safe responses, and escalates risky disputes.

---

## **Tech Stack**

* **Language:** Python 3.10+
* **Framework:** FastAPI, Pydantic v2
* **Web Server:** Uvicorn
* **HTTP Client:** HTTPX
* **AI Integration:** OpenAI Python SDK (compatible with any OpenAI-compatible API)
* **Testing:** Pytest

---

## **AI Approach & Hybrid Architecture**

To maximize accuracy, safety, and response speed under high load, this service implements a **Hybrid Architecture**:
1. **Deterministic Rules Engine (`app/rules.py`):** Parses amount patterns, translates Bangla numerals to standard digits, extracts phone numbers/counterparties, and resolves transaction matches. It deterministically assigns the `relevant_transaction_id`, `evidence_verdict`, `case_type`, `severity`, `department`, and `human_review_required` fields. This ensures 100% accuracy for routing and evidence evaluation.
2. **LLM Generation (`app/llm.py`):** Uses an OpenAI-compatible model to draft user-friendly descriptions (`agent_summary`, `recommended_next_action`) and translate responses (`customer_reply`) into the customer's native tongue (English or Bangla).
3. **Deterministic Safety Guard (`app/safety.py`):** A regex-based post-processor that intercepts the LLM output. If the LLM requests sensitive credentials (PIN/OTP/password) or promises unauthorized reversals/refunds, the guard overrides the reply with pre-vetted safe text.
4. **Failsafe Fallback:** If the LLM call fails, times out (5-second limit), or faces authentication/rate-limiting errors, the API falls back instantly to pre-translated templates, ensuring 100% availability.

---

## **MODELS Section**

| Model | Host / Provider | Purpose | Selection Reason |
| --- | --- | --- | --- |
| **`gpt-4o-mini`** (Default) | OpenAI | Drafting summaries, actions, and replies. | Excellent multilingual capability (handling Bangla and Banglish), rapid inference speeds under 1 second, and high cost-efficiency. |
| **Fallback Templates** | Local Rule Engine | Offline failsafe text generation. | Offline fallback guaranteeing zero downtime, zero network latency, and 100% safety protection in case of API outages. |

---

## **Safety Logic & Guardrails**

1. **Credentials Shield:** Scans `customer_reply` for keywords: `pin`, `otp`, `password`, `passcode`, `cvv`, `card number`, `পিন`, `ওটিপি`, `পাসওয়ার্ড`. If found in an active verb context (asking/requesting), replaces the reply with:
   *"We have received your concern. Please note that we never ask for your PIN, OTP, or password. Our support team will review the case and contact you shortly through official channels."*
2. **Refund Guarantee Shield:** Scrubs refund/reversal promises (e.g. "we will refund", "refund processed", or "money sent back") and replaces them with:
   *"Any eligible amount will be returned through official channels."*
3. **Third-Party Restriction:** Removes direct external URLs and telephone numbers, forcing direction to official customer service hotlines.

---

## **Setup & Installation**

### **Prerequisites**
* Python 3.9+ installed
* Pip package manager

### **Step-by-step Setup**
1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd Hackathon
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   Open `.env` and fill in your `OPENAI_API_KEY` and other custom API parameters if required.

---

## **Running the Service**

Run the service locally on port `8000`:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Verify the API is running by hitting the health check:
```bash
curl http://127.0.0.1:8000/health
# Expected Response: {"status":"ok"}
```

---

## **Running Tests**

To run the unit, API, safety, and compliance test suites, execute:
```bash
PYTHONPATH=. pytest -v
```

---

## **Assumptions & Known Limitations**

* **Amount Ambiguity:** If a user complains about sending a specific amount but there are multiple transactions in their history with the exact same amount, the engine tries to resolve it by matching counterparties. If no counterparties are mentioned, it reports `insufficient_data` and returns `null` for `relevant_transaction_id` to prevent raising incorrect disputes.
* **Banglish Translation:** The LLM's drafting quality relies on the provider's capability to understand Romanized Bangla (Banglish). The fallback engine handles standard English and Unicode Bangla perfectly.
