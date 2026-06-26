# QueueStorm Investigator — Design Specification

## Overview
An AI/API Copilot service for digital finance support agents, exposing `GET /health` and `POST /analyze-ticket`. It utilizes a hybrid approach: deterministic rules logic for high-accuracy reasoning, routing, and safety overrides, coupled with an OpenAI-compatible LLM for writing multilingual summaries and replies.

---

## 1. Architecture & Data Flow

The system consists of the following components:
1. **FastAPI Web Server:** Handles HTTP requests and schema validation.
2. **Deterministic Pre-processor (Rules Engine):** Programmatically resolves matching transaction IDs, evidence verdicts, routing department, severity, and human review flags.
3. **LLM Generator:** Submits the prompt to an OpenAI-compatible API to draft the agent summary, recommended action, and customer reply based on the verified pre-calculated variables.
4. **Deterministic Post-processor (Safety Guard):** Scrubs text outputs to filter out any sensitive credential requests or unauthorized refund promises before returning a response to the client.

```
[Client Request] ──► [FastAPI Schema Validation] ──► [Rules Engine] ──► [LLM Generation] ──► [Safety Guard] ──► [Response JSON]
```

---

## 2. Deterministic Rules Engine

### Amount Parsing
* Converts Bengali numerals (`০-৯`) to standard digits (`0-9`).
* Extracts all float/integer amounts from the complaint text using regular expressions.

### Counterparty & Transaction Matching
* Resolves `relevant_transaction_id` using a hierarchical matching logic:
  1. Filter transaction history for entries matching the parsed amounts.
  2. If multiple match, look for counterparty matches (checking for phone numbers, merchant IDs, agent IDs in the complaint text).
  3. If still ambiguous or multiple match with equal probability, set `relevant_transaction_id = null` and `evidence_verdict = "insufficient_data"`.
  4. If exactly one transaction matches:
     * Check pattern of recipient: If multiple successful past transfers exist to the same counterparty, and user claims "wrong transfer", set `evidence_verdict = "inconsistent"`.
     * Otherwise, compare transaction type and status with case indicators:
       * E.g. `payment_failed` requires a transaction status of `failed` or `pending`. If status is `completed` but user complains about failure, check for duplicates or flag `inconsistent`.
       * Set `evidence_verdict = "consistent"`.

### Case Type & Department Routing Taxonomy
We map key terms to case types and departments:
* `wrong_transfer` ──► `dispute_resolution` (Severity: High/Medium, Human Review: True)
* `payment_failed` ──► `payments_ops` (Severity: High, Human Review: False unless ambiguous)
* `refund_request` ──► `customer_support` (Severity: Low, Human Review: False)
* `duplicate_payment` ──► `payments_ops` (Severity: High, Human Review: True)
* `merchant_settlement_delay` ──► `merchant_operations` (Severity: Medium, Human Review: False)
* `agent_cash_in_issue` ──► `agent_operations` (Severity: High, Human Review: True)
* `phishing_or_social_engineering` ──► `fraud_risk` (Severity: Critical, Human Review: True)
* `other` ──► `customer_support` (Severity: Low, Human Review: False)

---

## 3. LLM Promoting & Response Generation

The LLM is invoked to generate:
1. `agent_summary`: 1-2 sentence operational summary.
2. `recommended_next_action`: Immediate next steps for support agents.
3. `customer_reply`: A safe, official reply matching the language of the complaint (English, Bangla).

### Fallback Mode
If the LLM call fails, times out, or has authentication issues, the service immediately falls back to deterministic template-based responses (using pre-translated templates for each `case_type`), ensuring 100% uptime and quick responses under pressure.

---

## 4. Safety Guard Post-Processor

The post-processor runs checks on `customer_reply` and `recommended_next_action`:
1. **Credentials Shield:** Rejects/removes phrases asking for PIN, OTP, password, or CVV. If triggered, replaces the reply with:
   *"We have received your concern. Please note that we never ask for your PIN, OTP, or password. Our support team will contact you shortly through official channels."*
2. **Refund Guarantee Shield:** Scrubs guarantees like "we will refund", "refund processed", or "money sent back". Replaces with:
   *"Any eligible amount will be returned through official channels."*
3. **Third-Party Restriction:** Removes external phone numbers, domains, or suspicious links, allowing only official channels.

---

## 5. Deployment & Runtime Constraints
* **Timeout Limit:** FastAPI handles request timing; LLM client call times out at 5 seconds, allowing ample time for fallback templates within the 30-second judge limit.
* **Port Binding:** Configured for `0.0.0.0` on port `8000`.
* **Zero Secrets Leakage:** No environment variables or credentials logged or sent in HTTP responses.
