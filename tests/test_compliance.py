import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_public_sample_cases():
    with open("Preliminary Questions and Resources/SUST_Preli_Sample_Cases.json", "r") as f:
        data = json.load(f)
    
    cases = data["cases"]
    sample_outputs = []
    
    for case in cases:
        case_id = case["id"]
        input_payload = case["input"]
        expected = case["expected_output"]
        
        response = client.post("/analyze-ticket", json=input_payload)
        assert response.status_code == 200, f"Case {case_id} failed"
        
        output = response.json()
        
        # Test required keys exist
        for key in ["ticket_id", "evidence_verdict", "case_type", "severity", "department", "agent_summary", "recommended_next_action", "customer_reply", "human_review_required"]:
            assert key in output, f"Missing key {key} in case {case_id}"
        
        # Compare core deterministic logic
        assert output["relevant_transaction_id"] == expected["relevant_transaction_id"], f"TX ID mismatch for {case_id}: expected {expected['relevant_transaction_id']}, got {output['relevant_transaction_id']}"
        assert output["evidence_verdict"] == expected["evidence_verdict"], f"Verdict mismatch for {case_id}: expected {expected['evidence_verdict']}, got {output['evidence_verdict']}"
        assert output["case_type"] == expected["case_type"], f"Case type mismatch for {case_id}: expected {expected['case_type']}, got {output['case_type']}"
        assert output["department"] == expected["department"], f"Department mismatch for {case_id}: expected {expected['department']}, got {output['department']}"
        
        # Collect one output for deliverables
        if case_id == "SAMPLE-01":
            sample_outputs.append({
                "case_id": case_id,
                "input": input_payload,
                "output": output
            })

    # Save deliverable case sample
    with open("queuestorm_sample_output.json", "w") as out_f:
        json.dump(sample_outputs, out_f, indent=2)
