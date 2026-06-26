from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_full_pipeline_payment_failed():
    payload = {
        "ticket_id": "TKT-100",
        "complaint": "I tried to pay 500 taka but it failed and balance deducted",
        "transaction_history": [
            {
                "transaction_id": "TXN-999",
                "timestamp": "2026-04-14T10:00:00Z",
                "type": "payment",
                "amount": 500,
                "counterparty": "MERCHANT-A",
                "status": "failed"
            }
        ]
    }
    response = client.post("/analyze-ticket", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["relevant_transaction_id"] == "TXN-999"
    assert data["evidence_verdict"] == "consistent"
    assert data["case_type"] == "payment_failed"
    assert "TXN-999" in data["customer_reply"]
