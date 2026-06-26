from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_analyze_ticket_mock():
    payload = {
        "ticket_id": "TKT-001",
        "complaint": "Test complaint"
    }
    response = client.post("/analyze-ticket", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["ticket_id"] == "TKT-001"
    assert data["evidence_verdict"] == "insufficient_data"
