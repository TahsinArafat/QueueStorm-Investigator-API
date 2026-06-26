This is the **QueueStorm Investigator** challenge — a hackathon problem asking you to build an **AI-powered support ticket analysis API** for a digital finance platform (think bKash). Here's everything broken down in detail:

---

## **The Scenario**

Imagine a massive cashback campaign is running on a mobile finance platform. By midnight, **40,000+ complaints** will flood into the support queue — wrong transfers, failed payments, scam attempts, refund requests, and more. Human agents can't keep up. Your job is to build an **AI copilot** that reads each complaint, cross-checks the customer's transaction history, and hands back a structured verdict to the support agent — all in under 30 seconds.\[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/157796097/ca651b6e-653e-46b3-817c-f92eff5f63ab/SUST_Hackathon_Preli_Problem_Statement.pdf?AWSAccessKeyId=ASIA2F3EMEYEXT2HOAWA&Signature=ox6sIDHi6W8%2F9iIHuJWXYkW2P5w%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEJ7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDJ9H8AN1TWvsQjAsgzhvFWj1H61nqz13p1e6fHwyBPFwIhAJ8Zi7L%2FiZ0srF%2BqziJJvOl4We4gNPVb3GtmKOC3fwDzKvMECGYQARoMNjk5NzUzMzA5NzA1Igwdrwq1R4oytWrTZ34q0AQw9O2%2FvXq1VHJUO%2Fq3Cjjzm%2BS%2BA7VgtzAzYJqo%2FCY%2FDiHQCW85BU5yhN51AEfpDQYxBJYJRTZNrsy6pq%2FoURJPjepFfJQ1dVvFQlfTVhIZG0eg4v2BB3vQ2t5GtVMwmR3%2ByG2qtEGA8W1mYG75iTVwl4PIAxOPFrekHwJwmRQiJvd1gyZaJGG9eiw2qS3lSruvFWg1eNfZnbKsGt46Ah%2Fs1JJWX6WUH8gnQH7qM1581hyj4%2BfqJmbBFLKIBOWwQ7sHbcUgn3pMpmWGLRQf8Msy6U%2BvBRA5qstIa7J1OtvIGMASdzlK3SRkrhezi5%2FjPchMCQw5VZ%2F%2Bl9eQj5ST8bCbj8wcWeJ8Hsrcz%2BnXqnU7dq4KPyr0gjWXJMujCkRkGUGpZp9cSOBObUJE03K7lW7C9299tm4o4vjRBT%2FIkqyq7EQdqrUvkdZTnlTWnAC%2BmM%2FsULAKnwOUc8VAxLbOmtsvZK%2BnSu6%2BC5eKszqSO9Jme9bTulkSYS5Uv1MqAaowZo%2Fe8hUKZOloQj1mi%2BCl%2BzNixrf1qX9m6tmF88by5r2HiwqWk0NBjFZKd6qYzxl6Hv6IVX2vhr4rWO%2FF34OjZFne0UR4KiIRNwtmuUXRPysobPDa%2F%2FW%2FBAWtWoP23P89MX99Eo11nta6%2BhBrbjbXUGBzaccv3pfj0QZ%2F121wRAk81CVsvb%2FHlhoUuNrfBweDLhl93wkCln5vJlklKgTgu6OK025bF0MLd4LiowPKlfgR8Rkw3VyiD6xq0GX4zsSlWZBttfiq%2FPZJjdnJSWOrIGaIMJ30%2BdEGOpcBq4l4bHcNpIAZWd2Bp%2FDLgg2g0OE3VLiVNUhWsY8mAqrKwQqr9KNRKRleDi7umZfF78FiZsr7w3ejgPsUBP2RowaBErGOMFqIq0neS8UXHT3o6jJ4juJGqssGQXkRdOFNFlgAyFBJnk3SA3EZ5Jor41iRd6qHSzGlcVK67%2FUn2Dy5UvsxhQ3Pef%2Fj%2B3oEqSJMuDp%2FYza5jg%3D%3D&Expires=1782482928)\]

---

## **What You're Building**

A **REST API service** with exactly two endpoints:\[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/157796097/ca651b6e-653e-46b3-817c-f92eff5f63ab/SUST_Hackathon_Preli_Problem_Statement.pdf?AWSAccessKeyId=ASIA2F3EMEYEXT2HOAWA&Signature=ox6sIDHi6W8%2F9iIHuJWXYkW2P5w%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEJ7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDJ9H8AN1TWvsQjAsgzhvFWj1H61nqz13p1e6fHwyBPFwIhAJ8Zi7L%2FiZ0srF%2BqziJJvOl4We4gNPVb3GtmKOC3fwDzKvMECGYQARoMNjk5NzUzMzA5NzA1Igwdrwq1R4oytWrTZ34q0AQw9O2%2FvXq1VHJUO%2Fq3Cjjzm%2BS%2BA7VgtzAzYJqo%2FCY%2FDiHQCW85BU5yhN51AEfpDQYxBJYJRTZNrsy6pq%2FoURJPjepFfJQ1dVvFQlfTVhIZG0eg4v2BB3vQ2t5GtVMwmR3%2ByG2qtEGA8W1mYG75iTVwl4PIAxOPFrekHwJwmRQiJvd1gyZaJGG9eiw2qS3lSruvFWg1eNfZnbKsGt46Ah%2Fs1JJWX6WUH8gnQH7qM1581hyj4%2BfqJmbBFLKIBOWwQ7sHbcUgn3pMpmWGLRQf8Msy6U%2BvBRA5qstIa7J1OtvIGMASdzlK3SRkrhezi5%2FjPchMCQw5VZ%2F%2Bl9eQj5ST8bCbj8wcWeJ8Hsrcz%2BnXqnU7dq4KPyr0gjWXJMujCkRkGUGpZp9cSOBObUJE03K7lW7C9299tm4o4vjRBT%2FIkqyq7EQdqrUvkdZTnlTWnAC%2BmM%2FsULAKnwOUc8VAxLbOmtsvZK%2BnSu6%2BC5eKszqSO9Jme9bTulkSYS5Uv1MqAaowZo%2Fe8hUKZOloQj1mi%2BCl%2BzNixrf1qX9m6tmF88by5r2HiwqWk0NBjFZKd6qYzxl6Hv6IVX2vhr4rWO%2FF34OjZFne0UR4KiIRNwtmuUXRPysobPDa%2F%2FW%2FBAWtWoP23P89MX99Eo11nta6%2BhBrbjbXUGBzaccv3pfj0QZ%2F121wRAk81CVsvb%2FHlhoUuNrfBweDLhl93wkCln5vJlklKgTgu6OK025bF0MLd4LiowPKlfgR8Rkw3VyiD6xq0GX4zsSlWZBttfiq%2FPZJjdnJSWOrIGaIMJ30%2BdEGOpcBq4l4bHcNpIAZWd2Bp%2FDLgg2g0OE3VLiVNUhWsY8mAqrKwQqr9KNRKRleDi7umZfF78FiZsr7w3ejgPsUBP2RowaBErGOMFqIq0neS8UXHT3o6jJ4juJGqssGQXkRdOFNFlgAyFBJnk3SA3EZ5Jor41iRd6qHSzGlcVK67%2FUn2Dy5UvsxhQ3Pef%2Fj%2B3oEqSJMuDp%2FYza5jg%3D%3D&Expires=1782482928)\]

| Endpoint | Purpose |
| ----- | ----- |
| `GET /health` | Returns `{"status":"ok"}` to confirm the service is running |
| `POST /analyze-ticket` | Accepts a complaint \+ transaction history, returns a structured JSON analysis |

You deploy this somewhere (live URL, Docker image, or code with runbook) and submit. The judge's automated harness will hit your API with hidden test cases.

---

## **The "Investigator Twist" — The Core Challenge**

This is **not just a text classifier**. It's an **evidence investigator**. Every request includes both:

1. The customer's **written complaint**  
2. Their **recent transaction history** (2–5 entries)

Your service must **cross-check** both. The complaint says one thing; the data might say something completely different. Two critical output fields capture this:\[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/157796097/ca651b6e-653e-46b3-817c-f92eff5f63ab/SUST_Hackathon_Preli_Problem_Statement.pdf?AWSAccessKeyId=ASIA2F3EMEYEXT2HOAWA&Signature=ox6sIDHi6W8%2F9iIHuJWXYkW2P5w%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEJ7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDJ9H8AN1TWvsQjAsgzhvFWj1H61nqz13p1e6fHwyBPFwIhAJ8Zi7L%2FiZ0srF%2BqziJJvOl4We4gNPVb3GtmKOC3fwDzKvMECGYQARoMNjk5NzUzMzA5NzA1Igwdrwq1R4oytWrTZ34q0AQw9O2%2FvXq1VHJUO%2Fq3Cjjzm%2BS%2BA7VgtzAzYJqo%2FCY%2FDiHQCW85BU5yhN51AEfpDQYxBJYJRTZNrsy6pq%2FoURJPjepFfJQ1dVvFQlfTVhIZG0eg4v2BB3vQ2t5GtVMwmR3%2ByG2qtEGA8W1mYG75iTVwl4PIAxOPFrekHwJwmRQiJvd1gyZaJGG9eiw2qS3lSruvFWg1eNfZnbKsGt46Ah%2Fs1JJWX6WUH8gnQH7qM1581hyj4%2BfqJmbBFLKIBOWwQ7sHbcUgn3pMpmWGLRQf8Msy6U%2BvBRA5qstIa7J1OtvIGMASdzlK3SRkrhezi5%2FjPchMCQw5VZ%2F%2Bl9eQj5ST8bCbj8wcWeJ8Hsrcz%2BnXqnU7dq4KPyr0gjWXJMujCkRkGUGpZp9cSOBObUJE03K7lW7C9299tm4o4vjRBT%2FIkqyq7EQdqrUvkdZTnlTWnAC%2BmM%2FsULAKnwOUc8VAxLbOmtsvZK%2BnSu6%2BC5eKszqSO9Jme9bTulkSYS5Uv1MqAaowZo%2Fe8hUKZOloQj1mi%2BCl%2BzNixrf1qX9m6tmF88by5r2HiwqWk0NBjFZKd6qYzxl6Hv6IVX2vhr4rWO%2FF34OjZFne0UR4KiIRNwtmuUXRPysobPDa%2F%2FW%2FBAWtWoP23P89MX99Eo11nta6%2BhBrbjbXUGBzaccv3pfj0QZ%2F121wRAk81CVsvb%2FHlhoUuNrfBweDLhl93wkCln5vJlklKgTgu6OK025bF0MLd4LiowPKlfgR8Rkw3VyiD6xq0GX4zsSlWZBttfiq%2FPZJjdnJSWOrIGaIMJ30%2BdEGOpcBq4l4bHcNpIAZWd2Bp%2FDLgg2g0OE3VLiVNUhWsY8mAqrKwQqr9KNRKRleDi7umZfF78FiZsr7w3ejgPsUBP2RowaBErGOMFqIq0neS8UXHT3o6jJ4juJGqssGQXkRdOFNFlgAyFBJnk3SA3EZ5Jor41iRd6qHSzGlcVK67%2FUn2Dy5UvsxhQ3Pef%2Fj%2B3oEqSJMuDp%2FYza5jg%3D%3D&Expires=1782482928)\]

* **`relevant_transaction_id`** — Which transaction in the history does the complaint refer to? (`null` if none matches)  
* **`evidence_verdict`** — One of:  
  * `consistent` → Transaction data *supports* the complaint  
  * `inconsistent` → Transaction data *contradicts* the complaint  
  * `insufficient_data` → Can't tell from the provided history

**Example:** Customer says "I sent 5000 taka to the wrong number." If transaction history shows a 5000 BDT transfer at the same time — verdict is `consistent`. If no such transaction exists — verdict is `insufficient_data`.

---

## **The Request (What Comes In)**

json  
`{`  
  `"ticket_id": "TKT-001",              ← required, must echo back in response`  
  `"complaint": "I sent 5000 taka...",  ← required (English, Bangla, or Banglish)`  
  `"language": "en",                    ← optional`  
  `"channel": "in_app_chat",            ← optional`  
  `"user_type": "customer",             ← optional`  
  `"campaign_context": "boishakh_...",  ← optional`  
  `"transaction_history": [...]         ← optional array of recent txns`  
`}`

Each transaction entry has: `transaction_id`, `timestamp`, `type` (transfer/payment/cash\_in/cash\_out/settlement/refund), `amount` (BDT), `counterparty`, `status` (completed/failed/pending/reversed).\[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/157796097/ca651b6e-653e-46b3-817c-f92eff5f63ab/SUST_Hackathon_Preli_Problem_Statement.pdf?AWSAccessKeyId=ASIA2F3EMEYEXT2HOAWA&Signature=ox6sIDHi6W8%2F9iIHuJWXYkW2P5w%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEJ7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDJ9H8AN1TWvsQjAsgzhvFWj1H61nqz13p1e6fHwyBPFwIhAJ8Zi7L%2FiZ0srF%2BqziJJvOl4We4gNPVb3GtmKOC3fwDzKvMECGYQARoMNjk5NzUzMzA5NzA1Igwdrwq1R4oytWrTZ34q0AQw9O2%2FvXq1VHJUO%2Fq3Cjjzm%2BS%2BA7VgtzAzYJqo%2FCY%2FDiHQCW85BU5yhN51AEfpDQYxBJYJRTZNrsy6pq%2FoURJPjepFfJQ1dVvFQlfTVhIZG0eg4v2BB3vQ2t5GtVMwmR3%2ByG2qtEGA8W1mYG75iTVwl4PIAxOPFrekHwJwmRQiJvd1gyZaJGG9eiw2qS3lSruvFWg1eNfZnbKsGt46Ah%2Fs1JJWX6WUH8gnQH7qM1581hyj4%2BfqJmbBFLKIBOWwQ7sHbcUgn3pMpmWGLRQf8Msy6U%2BvBRA5qstIa7J1OtvIGMASdzlK3SRkrhezi5%2FjPchMCQw5VZ%2F%2Bl9eQj5ST8bCbj8wcWeJ8Hsrcz%2BnXqnU7dq4KPyr0gjWXJMujCkRkGUGpZp9cSOBObUJE03K7lW7C9299tm4o4vjRBT%2FIkqyq7EQdqrUvkdZTnlTWnAC%2BmM%2FsULAKnwOUc8VAxLbOmtsvZK%2BnSu6%2BC5eKszqSO9Jme9bTulkSYS5Uv1MqAaowZo%2Fe8hUKZOloQj1mi%2BCl%2BzNixrf1qX9m6tmF88by5r2HiwqWk0NBjFZKd6qYzxl6Hv6IVX2vhr4rWO%2FF34OjZFne0UR4KiIRNwtmuUXRPysobPDa%2F%2FW%2FBAWtWoP23P89MX99Eo11nta6%2BhBrbjbXUGBzaccv3pfj0QZ%2F121wRAk81CVsvb%2FHlhoUuNrfBweDLhl93wkCln5vJlklKgTgu6OK025bF0MLd4LiowPKlfgR8Rkw3VyiD6xq0GX4zsSlWZBttfiq%2FPZJjdnJSWOrIGaIMJ30%2BdEGOpcBq4l4bHcNpIAZWd2Bp%2FDLgg2g0OE3VLiVNUhWsY8mAqrKwQqr9KNRKRleDi7umZfF78FiZsr7w3ejgPsUBP2RowaBErGOMFqIq0neS8UXHT3o6jJ4juJGqssGQXkRdOFNFlgAyFBJnk3SA3EZ5Jor41iRd6qHSzGlcVK67%2FUn2Dy5UvsxhQ3Pef%2Fj%2B3oEqSJMuDp%2FYza5jg%3D%3D&Expires=1782482928)\]

---

## **The Response (What You Must Return)**

Your API must return all of these:\[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/157796097/ca651b6e-653e-46b3-817c-f92eff5f63ab/SUST_Hackathon_Preli_Problem_Statement.pdf?AWSAccessKeyId=ASIA2F3EMEYEXT2HOAWA&Signature=ox6sIDHi6W8%2F9iIHuJWXYkW2P5w%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEJ7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDJ9H8AN1TWvsQjAsgzhvFWj1H61nqz13p1e6fHwyBPFwIhAJ8Zi7L%2FiZ0srF%2BqziJJvOl4We4gNPVb3GtmKOC3fwDzKvMECGYQARoMNjk5NzUzMzA5NzA1Igwdrwq1R4oytWrTZ34q0AQw9O2%2FvXq1VHJUO%2Fq3Cjjzm%2BS%2BA7VgtzAzYJqo%2FCY%2FDiHQCW85BU5yhN51AEfpDQYxBJYJRTZNrsy6pq%2FoURJPjepFfJQ1dVvFQlfTVhIZG0eg4v2BB3vQ2t5GtVMwmR3%2ByG2qtEGA8W1mYG75iTVwl4PIAxOPFrekHwJwmRQiJvd1gyZaJGG9eiw2qS3lSruvFWg1eNfZnbKsGt46Ah%2Fs1JJWX6WUH8gnQH7qM1581hyj4%2BfqJmbBFLKIBOWwQ7sHbcUgn3pMpmWGLRQf8Msy6U%2BvBRA5qstIa7J1OtvIGMASdzlK3SRkrhezi5%2FjPchMCQw5VZ%2F%2Bl9eQj5ST8bCbj8wcWeJ8Hsrcz%2BnXqnU7dq4KPyr0gjWXJMujCkRkGUGpZp9cSOBObUJE03K7lW7C9299tm4o4vjRBT%2FIkqyq7EQdqrUvkdZTnlTWnAC%2BmM%2FsULAKnwOUc8VAxLbOmtsvZK%2BnSu6%2BC5eKszqSO9Jme9bTulkSYS5Uv1MqAaowZo%2Fe8hUKZOloQj1mi%2BCl%2BzNixrf1qX9m6tmF88by5r2HiwqWk0NBjFZKd6qYzxl6Hv6IVX2vhr4rWO%2FF34OjZFne0UR4KiIRNwtmuUXRPysobPDa%2F%2FW%2FBAWtWoP23P89MX99Eo11nta6%2BhBrbjbXUGBzaccv3pfj0QZ%2F121wRAk81CVsvb%2FHlhoUuNrfBweDLhl93wkCln5vJlklKgTgu6OK025bF0MLd4LiowPKlfgR8Rkw3VyiD6xq0GX4zsSlWZBttfiq%2FPZJjdnJSWOrIGaIMJ30%2BdEGOpcBq4l4bHcNpIAZWd2Bp%2FDLgg2g0OE3VLiVNUhWsY8mAqrKwQqr9KNRKRleDi7umZfF78FiZsr7w3ejgPsUBP2RowaBErGOMFqIq0neS8UXHT3o6jJ4juJGqssGQXkRdOFNFlgAyFBJnk3SA3EZ5Jor41iRd6qHSzGlcVK67%2FUn2Dy5UvsxhQ3Pef%2Fj%2B3oEqSJMuDp%2FYza5jg%3D%3D&Expires=1782482928)\]

| Field | Description |
| ----- | ----- |
| `ticket_id` | Echo back exactly what was sent |
| `relevant_transaction_id` | Matching TXN ID or `null` |
| `evidence_verdict` | `consistent` / `inconsistent` / `insufficient_data` |
| `case_type` | Category of the complaint (see taxonomy below) |
| `severity` | `low` / `medium` / `high` / `critical` |
| `department` | Which team should handle it |
| `agent_summary` | 1–2 sentence summary for the support agent |
| `recommended_next_action` | What the agent should do next |
| `customer_reply` | A safe, pre-drafted reply to the customer |
| `human_review_required` | `true`/`false` — escalate if risky or ambiguous |
| `confidence` | Optional float 0–1 |
| `reason_codes` | Optional short labels like `["wrong_transfer", "transaction_match"]` |

---

## **Case Types & Department Routing**

**`case_type` values**:\[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/157796097/ca651b6e-653e-46b3-817c-f92eff5f63ab/SUST_Hackathon_Preli_Problem_Statement.pdf?AWSAccessKeyId=ASIA2F3EMEYEXT2HOAWA&Signature=ox6sIDHi6W8%2F9iIHuJWXYkW2P5w%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEJ7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDJ9H8AN1TWvsQjAsgzhvFWj1H61nqz13p1e6fHwyBPFwIhAJ8Zi7L%2FiZ0srF%2BqziJJvOl4We4gNPVb3GtmKOC3fwDzKvMECGYQARoMNjk5NzUzMzA5NzA1Igwdrwq1R4oytWrTZ34q0AQw9O2%2FvXq1VHJUO%2Fq3Cjjzm%2BS%2BA7VgtzAzYJqo%2FCY%2FDiHQCW85BU5yhN51AEfpDQYxBJYJRTZNrsy6pq%2FoURJPjepFfJQ1dVvFQlfTVhIZG0eg4v2BB3vQ2t5GtVMwmR3%2ByG2qtEGA8W1mYG75iTVwl4PIAxOPFrekHwJwmRQiJvd1gyZaJGG9eiw2qS3lSruvFWg1eNfZnbKsGt46Ah%2Fs1JJWX6WUH8gnQH7qM1581hyj4%2BfqJmbBFLKIBOWwQ7sHbcUgn3pMpmWGLRQf8Msy6U%2BvBRA5qstIa7J1OtvIGMASdzlK3SRkrhezi5%2FjPchMCQw5VZ%2F%2Bl9eQj5ST8bCbj8wcWeJ8Hsrcz%2BnXqnU7dq4KPyr0gjWXJMujCkRkGUGpZp9cSOBObUJE03K7lW7C9299tm4o4vjRBT%2FIkqyq7EQdqrUvkdZTnlTWnAC%2BmM%2FsULAKnwOUc8VAxLbOmtsvZK%2BnSu6%2BC5eKszqSO9Jme9bTulkSYS5Uv1MqAaowZo%2Fe8hUKZOloQj1mi%2BCl%2BzNixrf1qX9m6tmF88by5r2HiwqWk0NBjFZKd6qYzxl6Hv6IVX2vhr4rWO%2FF34OjZFne0UR4KiIRNwtmuUXRPysobPDa%2F%2FW%2FBAWtWoP23P89MX99Eo11nta6%2BhBrbjbXUGBzaccv3pfj0QZ%2F121wRAk81CVsvb%2FHlhoUuNrfBweDLhl93wkCln5vJlklKgTgu6OK025bF0MLd4LiowPKlfgR8Rkw3VyiD6xq0GX4zsSlWZBttfiq%2FPZJjdnJSWOrIGaIMJ30%2BdEGOpcBq4l4bHcNpIAZWd2Bp%2FDLgg2g0OE3VLiVNUhWsY8mAqrKwQqr9KNRKRleDi7umZfF78FiZsr7w3ejgPsUBP2RowaBErGOMFqIq0neS8UXHT3o6jJ4juJGqssGQXkRdOFNFlgAyFBJnk3SA3EZ5Jor41iRd6qHSzGlcVK67%2FUn2Dy5UvsxhQ3Pef%2Fj%2B3oEqSJMuDp%2FYza5jg%3D%3D&Expires=1782482928)\]

* `wrong_transfer` → money sent to wrong person  
* `payment_failed` → failed but balance deducted  
* `refund_request` → customer wants money back  
* `duplicate_payment` → charged twice  
* `merchant_settlement_delay` → merchant didn't receive settlement  
* `agent_cash_in_issue` → cash deposit not reflected  
* `phishing_or_social_engineering` → scam/fraud attempt  
* `other` → anything else

**`department` routing**:\[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/157796097/ca651b6e-653e-46b3-817c-f92eff5f63ab/SUST_Hackathon_Preli_Problem_Statement.pdf?AWSAccessKeyId=ASIA2F3EMEYEXT2HOAWA&Signature=ox6sIDHi6W8%2F9iIHuJWXYkW2P5w%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEJ7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDJ9H8AN1TWvsQjAsgzhvFWj1H61nqz13p1e6fHwyBPFwIhAJ8Zi7L%2FiZ0srF%2BqziJJvOl4We4gNPVb3GtmKOC3fwDzKvMECGYQARoMNjk5NzUzMzA5NzA1Igwdrwq1R4oytWrTZ34q0AQw9O2%2FvXq1VHJUO%2Fq3Cjjzm%2BS%2BA7VgtzAzYJqo%2FCY%2FDiHQCW85BU5yhN51AEfpDQYxBJYJRTZNrsy6pq%2FoURJPjepFfJQ1dVvFQlfTVhIZG0eg4v2BB3vQ2t5GtVMwmR3%2ByG2qtEGA8W1mYG75iTVwl4PIAxOPFrekHwJwmRQiJvd1gyZaJGG9eiw2qS3lSruvFWg1eNfZnbKsGt46Ah%2Fs1JJWX6WUH8gnQH7qM1581hyj4%2BfqJmbBFLKIBOWwQ7sHbcUgn3pMpmWGLRQf8Msy6U%2BvBRA5qstIa7J1OtvIGMASdzlK3SRkrhezi5%2FjPchMCQw5VZ%2F%2Bl9eQj5ST8bCbj8wcWeJ8Hsrcz%2BnXqnU7dq4KPyr0gjWXJMujCkRkGUGpZp9cSOBObUJE03K7lW7C9299tm4o4vjRBT%2FIkqyq7EQdqrUvkdZTnlTWnAC%2BmM%2FsULAKnwOUc8VAxLbOmtsvZK%2BnSu6%2BC5eKszqSO9Jme9bTulkSYS5Uv1MqAaowZo%2Fe8hUKZOloQj1mi%2BCl%2BzNixrf1qX9m6tmF88by5r2HiwqWk0NBjFZKd6qYzxl6Hv6IVX2vhr4rWO%2FF34OjZFne0UR4KiIRNwtmuUXRPysobPDa%2F%2FW%2FBAWtWoP23P89MX99Eo11nta6%2BhBrbjbXUGBzaccv3pfj0QZ%2F121wRAk81CVsvb%2FHlhoUuNrfBweDLhl93wkCln5vJlklKgTgu6OK025bF0MLd4LiowPKlfgR8Rkw3VyiD6xq0GX4zsSlWZBttfiq%2FPZJjdnJSWOrIGaIMJ30%2BdEGOpcBq4l4bHcNpIAZWd2Bp%2FDLgg2g0OE3VLiVNUhWsY8mAqrKwQqr9KNRKRleDi7umZfF78FiZsr7w3ejgPsUBP2RowaBErGOMFqIq0neS8UXHT3o6jJ4juJGqssGQXkRdOFNFlgAyFBJnk3SA3EZ5Jor41iRd6qHSzGlcVK67%2FUn2Dy5UvsxhQ3Pef%2Fj%2B3oEqSJMuDp%2FYza5jg%3D%3D&Expires=1782482928)\]

* `customer_support` → general/low-severity cases  
* `dispute_resolution` → wrong transfers, contested refunds  
* `payments_ops` → failed/duplicate payments  
* `merchant_operations` → merchant complaints  
* `agent_operations` → agent complaints  
* `fraud_risk` → phishing/suspicious cases

---

## **Safety Rules — Critical, Penalized Automatically**

These are hard rules your `customer_reply` must never violate:\[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/157796097/ca651b6e-653e-46b3-817c-f92eff5f63ab/SUST_Hackathon_Preli_Problem_Statement.pdf?AWSAccessKeyId=ASIA2F3EMEYEXT2HOAWA&Signature=ox6sIDHi6W8%2F9iIHuJWXYkW2P5w%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEJ7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDJ9H8AN1TWvsQjAsgzhvFWj1H61nqz13p1e6fHwyBPFwIhAJ8Zi7L%2FiZ0srF%2BqziJJvOl4We4gNPVb3GtmKOC3fwDzKvMECGYQARoMNjk5NzUzMzA5NzA1Igwdrwq1R4oytWrTZ34q0AQw9O2%2FvXq1VHJUO%2Fq3Cjjzm%2BS%2BA7VgtzAzYJqo%2FCY%2FDiHQCW85BU5yhN51AEfpDQYxBJYJRTZNrsy6pq%2FoURJPjepFfJQ1dVvFQlfTVhIZG0eg4v2BB3vQ2t5GtVMwmR3%2ByG2qtEGA8W1mYG75iTVwl4PIAxOPFrekHwJwmRQiJvd1gyZaJGG9eiw2qS3lSruvFWg1eNfZnbKsGt46Ah%2Fs1JJWX6WUH8gnQH7qM1581hyj4%2BfqJmbBFLKIBOWwQ7sHbcUgn3pMpmWGLRQf8Msy6U%2BvBRA5qstIa7J1OtvIGMASdzlK3SRkrhezi5%2FjPchMCQw5VZ%2F%2Bl9eQj5ST8bCbj8wcWeJ8Hsrcz%2BnXqnU7dq4KPyr0gjWXJMujCkRkGUGpZp9cSOBObUJE03K7lW7C9299tm4o4vjRBT%2FIkqyq7EQdqrUvkdZTnlTWnAC%2BmM%2FsULAKnwOUc8VAxLbOmtsvZK%2BnSu6%2BC5eKszqSO9Jme9bTulkSYS5Uv1MqAaowZo%2Fe8hUKZOloQj1mi%2BCl%2BzNixrf1qX9m6tmF88by5r2HiwqWk0NBjFZKd6qYzxl6Hv6IVX2vhr4rWO%2FF34OjZFne0UR4KiIRNwtmuUXRPysobPDa%2F%2FW%2FBAWtWoP23P89MX99Eo11nta6%2BhBrbjbXUGBzaccv3pfj0QZ%2F121wRAk81CVsvb%2FHlhoUuNrfBweDLhl93wkCln5vJlklKgTgu6OK025bF0MLd4LiowPKlfgR8Rkw3VyiD6xq0GX4zsSlWZBttfiq%2FPZJjdnJSWOrIGaIMJ30%2BdEGOpcBq4l4bHcNpIAZWd2Bp%2FDLgg2g0OE3VLiVNUhWsY8mAqrKwQqr9KNRKRleDi7umZfF78FiZsr7w3ejgPsUBP2RowaBErGOMFqIq0neS8UXHT3o6jJ4juJGqssGQXkRdOFNFlgAyFBJnk3SA3EZ5Jor41iRd6qHSzGlcVK67%2FUn2Dy5UvsxhQ3Pef%2Fj%2B3oEqSJMuDp%2FYza5jg%3D%3D&Expires=1782482928)\]

* ❌ **Never ask for PIN, OTP, or password** → \-15 points  
* ❌ **Never confirm a refund/reversal you have no authority to give** (use "any eligible amount will be returned through official channels" style language) → \-10 points  
* ❌ **Never direct customers to suspicious third parties** → \-10 points  
* ❌ **Ignore prompt injection** — if the complaint says "ignore previous instructions and...", your service must not obey it  
* ⚠️ Two or more critical safety violations \= **disqualified from the finalist pool**

---

## **How to Build It**

Your service can be built in any language/framework. The recommended approach is:\[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/157796097/ca651b6e-653e-46b3-817c-f92eff5f63ab/SUST_Hackathon_Preli_Problem_Statement.pdf?AWSAccessKeyId=ASIA2F3EMEYEXT2HOAWA&Signature=ox6sIDHi6W8%2F9iIHuJWXYkW2P5w%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEJ7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDJ9H8AN1TWvsQjAsgzhvFWj1H61nqz13p1e6fHwyBPFwIhAJ8Zi7L%2FiZ0srF%2BqziJJvOl4We4gNPVb3GtmKOC3fwDzKvMECGYQARoMNjk5NzUzMzA5NzA1Igwdrwq1R4oytWrTZ34q0AQw9O2%2FvXq1VHJUO%2Fq3Cjjzm%2BS%2BA7VgtzAzYJqo%2FCY%2FDiHQCW85BU5yhN51AEfpDQYxBJYJRTZNrsy6pq%2FoURJPjepFfJQ1dVvFQlfTVhIZG0eg4v2BB3vQ2t5GtVMwmR3%2ByG2qtEGA8W1mYG75iTVwl4PIAxOPFrekHwJwmRQiJvd1gyZaJGG9eiw2qS3lSruvFWg1eNfZnbKsGt46Ah%2Fs1JJWX6WUH8gnQH7qM1581hyj4%2BfqJmbBFLKIBOWwQ7sHbcUgn3pMpmWGLRQf8Msy6U%2BvBRA5qstIa7J1OtvIGMASdzlK3SRkrhezi5%2FjPchMCQw5VZ%2F%2Bl9eQj5ST8bCbj8wcWeJ8Hsrcz%2BnXqnU7dq4KPyr0gjWXJMujCkRkGUGpZp9cSOBObUJE03K7lW7C9299tm4o4vjRBT%2FIkqyq7EQdqrUvkdZTnlTWnAC%2BmM%2FsULAKnwOUc8VAxLbOmtsvZK%2BnSu6%2BC5eKszqSO9Jme9bTulkSYS5Uv1MqAaowZo%2Fe8hUKZOloQj1mi%2BCl%2BzNixrf1qX9m6tmF88by5r2HiwqWk0NBjFZKd6qYzxl6Hv6IVX2vhr4rWO%2FF34OjZFne0UR4KiIRNwtmuUXRPysobPDa%2F%2FW%2FBAWtWoP23P89MX99Eo11nta6%2BhBrbjbXUGBzaccv3pfj0QZ%2F121wRAk81CVsvb%2FHlhoUuNrfBweDLhl93wkCln5vJlklKgTgu6OK025bF0MLd4LiowPKlfgR8Rkw3VyiD6xq0GX4zsSlWZBttfiq%2FPZJjdnJSWOrIGaIMJ30%2BdEGOpcBq4l4bHcNpIAZWd2Bp%2FDLgg2g0OE3VLiVNUhWsY8mAqrKwQqr9KNRKRleDi7umZfF78FiZsr7w3ejgPsUBP2RowaBErGOMFqIq0neS8UXHT3o6jJ4juJGqssGQXkRdOFNFlgAyFBJnk3SA3EZ5Jor41iRd6qHSzGlcVK67%2FUn2Dy5UvsxhQ3Pef%2Fj%2B3oEqSJMuDp%2FYza5jg%3D%3D&Expires=1782482928)\]

1. **Parse** the incoming JSON complaint \+ transaction history  
2. **Use an LLM** (OpenAI, Anthropic, Gemini, Cohere, etc. — you supply the API key) or rule-based logic to analyze  
3. **Return** the fully structured JSON response  
4. **Deploy** on Render, Railway, Fly.io, Vercel, AWS, or Poridhi Labs

**Runtime constraints:** Must respond within **30 seconds** per request, and `GET /health` must be ready within **60 seconds** of service start.\[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/157796097/ca651b6e-653e-46b3-817c-f92eff5f63ab/SUST_Hackathon_Preli_Problem_Statement.pdf?AWSAccessKeyId=ASIA2F3EMEYEXT2HOAWA&Signature=ox6sIDHi6W8%2F9iIHuJWXYkW2P5w%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEJ7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDJ9H8AN1TWvsQjAsgzhvFWj1H61nqz13p1e6fHwyBPFwIhAJ8Zi7L%2FiZ0srF%2BqziJJvOl4We4gNPVb3GtmKOC3fwDzKvMECGYQARoMNjk5NzUzMzA5NzA1Igwdrwq1R4oytWrTZ34q0AQw9O2%2FvXq1VHJUO%2Fq3Cjjzm%2BS%2BA7VgtzAzYJqo%2FCY%2FDiHQCW85BU5yhN51AEfpDQYxBJYJRTZNrsy6pq%2FoURJPjepFfJQ1dVvFQlfTVhIZG0eg4v2BB3vQ2t5GtVMwmR3%2ByG2qtEGA8W1mYG75iTVwl4PIAxOPFrekHwJwmRQiJvd1gyZaJGG9eiw2qS3lSruvFWg1eNfZnbKsGt46Ah%2Fs1JJWX6WUH8gnQH7qM1581hyj4%2BfqJmbBFLKIBOWwQ7sHbcUgn3pMpmWGLRQf8Msy6U%2BvBRA5qstIa7J1OtvIGMASdzlK3SRkrhezi5%2FjPchMCQw5VZ%2F%2Bl9eQj5ST8bCbj8wcWeJ8Hsrcz%2BnXqnU7dq4KPyr0gjWXJMujCkRkGUGpZp9cSOBObUJE03K7lW7C9299tm4o4vjRBT%2FIkqyq7EQdqrUvkdZTnlTWnAC%2BmM%2FsULAKnwOUc8VAxLbOmtsvZK%2BnSu6%2BC5eKszqSO9Jme9bTulkSYS5Uv1MqAaowZo%2Fe8hUKZOloQj1mi%2BCl%2BzNixrf1qX9m6tmF88by5r2HiwqWk0NBjFZKd6qYzxl6Hv6IVX2vhr4rWO%2FF34OjZFne0UR4KiIRNwtmuUXRPysobPDa%2F%2FW%2FBAWtWoP23P89MX99Eo11nta6%2BhBrbjbXUGBzaccv3pfj0QZ%2F121wRAk81CVsvb%2FHlhoUuNrfBweDLhl93wkCln5vJlklKgTgu6OK025bF0MLd4LiowPKlfgR8Rkw3VyiD6xq0GX4zsSlWZBttfiq%2FPZJjdnJSWOrIGaIMJ30%2BdEGOpcBq4l4bHcNpIAZWd2Bp%2FDLgg2g0OE3VLiVNUhWsY8mAqrKwQqr9KNRKRleDi7umZfF78FiZsr7w3ejgPsUBP2RowaBErGOMFqIq0neS8UXHT3o6jJ4juJGqssGQXkRdOFNFlgAyFBJnk3SA3EZ5Jor41iRd6qHSzGlcVK67%2FUn2Dy5UvsxhQ3Pef%2Fj%2B3oEqSJMuDp%2FYza5jg%3D%3D&Expires=1782482928)\]

---

## **Scoring Breakdown**

| Category | Weight |
| ----- | ----- |
| Evidence Reasoning (right verdict, classification, routing) | 35% |
| Safety & Escalation | 20% |
| API Contract & Schema correctness | 15% |
| Performance & Reliability | 10% |
| Response Quality | 10% |
| Deployment & Reproducibility | 5% |
| Documentation (README) | 5% |

---

## **What to Submit**

1. **GitHub repo** (public, accessible to `bipulhf`) with all code\[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/157796097/ca651b6e-653e-46b3-817c-f92eff5f63ab/SUST_Hackathon_Preli_Problem_Statement.pdf?AWSAccessKeyId=ASIA2F3EMEYEXT2HOAWA&Signature=ox6sIDHi6W8%2F9iIHuJWXYkW2P5w%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEJ7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDJ9H8AN1TWvsQjAsgzhvFWj1H61nqz13p1e6fHwyBPFwIhAJ8Zi7L%2FiZ0srF%2BqziJJvOl4We4gNPVb3GtmKOC3fwDzKvMECGYQARoMNjk5NzUzMzA5NzA1Igwdrwq1R4oytWrTZ34q0AQw9O2%2FvXq1VHJUO%2Fq3Cjjzm%2BS%2BA7VgtzAzYJqo%2FCY%2FDiHQCW85BU5yhN51AEfpDQYxBJYJRTZNrsy6pq%2FoURJPjepFfJQ1dVvFQlfTVhIZG0eg4v2BB3vQ2t5GtVMwmR3%2ByG2qtEGA8W1mYG75iTVwl4PIAxOPFrekHwJwmRQiJvd1gyZaJGG9eiw2qS3lSruvFWg1eNfZnbKsGt46Ah%2Fs1JJWX6WUH8gnQH7qM1581hyj4%2BfqJmbBFLKIBOWwQ7sHbcUgn3pMpmWGLRQf8Msy6U%2BvBRA5qstIa7J1OtvIGMASdzlK3SRkrhezi5%2FjPchMCQw5VZ%2F%2Bl9eQj5ST8bCbj8wcWeJ8Hsrcz%2BnXqnU7dq4KPyr0gjWXJMujCkRkGUGpZp9cSOBObUJE03K7lW7C9299tm4o4vjRBT%2FIkqyq7EQdqrUvkdZTnlTWnAC%2BmM%2FsULAKnwOUc8VAxLbOmtsvZK%2BnSu6%2BC5eKszqSO9Jme9bTulkSYS5Uv1MqAaowZo%2Fe8hUKZOloQj1mi%2BCl%2BzNixrf1qX9m6tmF88by5r2HiwqWk0NBjFZKd6qYzxl6Hv6IVX2vhr4rWO%2FF34OjZFne0UR4KiIRNwtmuUXRPysobPDa%2F%2FW%2FBAWtWoP23P89MX99Eo11nta6%2BhBrbjbXUGBzaccv3pfj0QZ%2F121wRAk81CVsvb%2FHlhoUuNrfBweDLhl93wkCln5vJlklKgTgu6OK025bF0MLd4LiowPKlfgR8Rkw3VyiD6xq0GX4zsSlWZBttfiq%2FPZJjdnJSWOrIGaIMJ30%2BdEGOpcBq4l4bHcNpIAZWd2Bp%2FDLgg2g0OE3VLiVNUhWsY8mAqrKwQqr9KNRKRleDi7umZfF78FiZsr7w3ejgPsUBP2RowaBErGOMFqIq0neS8UXHT3o6jJ4juJGqssGQXkRdOFNFlgAyFBJnk3SA3EZ5Jor41iRd6qHSzGlcVK67%2FUn2Dy5UvsxhQ3Pef%2Fj%2B3oEqSJMuDp%2FYza5jg%3D%3D&Expires=1782482928)\]  
2. **Live URL** (strongly preferred) — or Docker image — or code \+ runbook  
3. **README.md** with tech stack, AI approach, safety logic, model choices  
4. **Sample output file** generated from the provided 10 sample cases  
5. Optional but recommended: a **90-second architecture walkthrough video**

---

## **TL;DR — What You Actually Code**

You're building a **FastAPI/Express/Next.js app** that:

1. Receives a support ticket with transaction history  
2. Calls an LLM with a well-crafted prompt  
3. Makes the LLM reason about whether the complaint matches the data  
4. Returns a clean, schema-valid JSON with classification, routing, evidence verdict, a safe customer reply, and an agent action — all while **never leaking credentials or confirming unauthorized refunds**\[[ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/157796097/ca651b6e-653e-46b3-817c-f92eff5f63ab/SUST_Hackathon_Preli_Problem_Statement.pdf?AWSAccessKeyId=ASIA2F3EMEYEXT2HOAWA&Signature=ox6sIDHi6W8%2F9iIHuJWXYkW2P5w%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEJ7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDJ9H8AN1TWvsQjAsgzhvFWj1H61nqz13p1e6fHwyBPFwIhAJ8Zi7L%2FiZ0srF%2BqziJJvOl4We4gNPVb3GtmKOC3fwDzKvMECGYQARoMNjk5NzUzMzA5NzA1Igwdrwq1R4oytWrTZ34q0AQw9O2%2FvXq1VHJUO%2Fq3Cjjzm%2BS%2BA7VgtzAzYJqo%2FCY%2FDiHQCW85BU5yhN51AEfpDQYxBJYJRTZNrsy6pq%2FoURJPjepFfJQ1dVvFQlfTVhIZG0eg4v2BB3vQ2t5GtVMwmR3%2ByG2qtEGA8W1mYG75iTVwl4PIAxOPFrekHwJwmRQiJvd1gyZaJGG9eiw2qS3lSruvFWg1eNfZnbKsGt46Ah%2Fs1JJWX6WUH8gnQH7qM1581hyj4%2BfqJmbBFLKIBOWwQ7sHbcUgn3pMpmWGLRQf8Msy6U%2BvBRA5qstIa7J1OtvIGMASdzlK3SRkrhezi5%2FjPchMCQw5VZ%2F%2Bl9eQj5ST8bCbj8wcWeJ8Hsrcz%2BnXqnU7dq4KPyr0gjWXJMujCkRkGUGpZp9cSOBObUJE03K7lW7C9299tm4o4vjRBT%2FIkqyq7EQdqrUvkdZTnlTWnAC%2BmM%2FsULAKnwOUc8VAxLbOmtsvZK%2BnSu6%2BC5eKszqSO9Jme9bTulkSYS5Uv1MqAaowZo%2Fe8hUKZOloQj1mi%2BCl%2BzNixrf1qX9m6tmF88by5r2HiwqWk0NBjFZKd6qYzxl6Hv6IVX2vhr4rWO%2FF34OjZFne0UR4KiIRNwtmuUXRPysobPDa%2F%2FW%2FBAWtWoP23P89MX99Eo11nta6%2BhBrbjbXUGBzaccv3pfj0QZ%2F121wRAk81CVsvb%2FHlhoUuNrfBweDLhl93wkCln5vJlklKgTgu6OK025bF0MLd4LiowPKlfgR8Rkw3VyiD6xq0GX4zsSlWZBttfiq%2FPZJjdnJSWOrIGaIMJ30%2BdEGOpcBq4l4bHcNpIAZWd2Bp%2FDLgg2g0OE3VLiVNUhWsY8mAqrKwQqr9KNRKRleDi7umZfF78FiZsr7w3ejgPsUBP2RowaBErGOMFqIq0neS8UXHT3o6jJ4juJGqssGQXkRdOFNFlgAyFBJnk3SA3EZ5Jor41iRd6qHSzGlcVK67%2FUn2Dy5UvsxhQ3Pef%2Fj%2B3oEqSJMuDp%2FYza5jg%3D%3D&Expires=1782482928)\]

