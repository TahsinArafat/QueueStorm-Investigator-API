import json
import httpx
import sys

# Load sample cases
with open("Preliminary Questions and Resources/SUST_Preli_Sample_Cases.json") as f:
    data = json.load(f)

results = []
passed = 0
failed = 0

print("Testing all 10 sample cases against the API...\n")

for case in data["cases"]:
    case_id = case["id"]
    case_label = case["label"]
    input_data = case["input"]
    expected = case["expected_output"]
    
    try:
        response = httpx.post(
            "http://127.0.0.1:8000/analyze-ticket",
            json=input_data,
            timeout=30.0
        )
        
        if response.status_code != 200:
            print(f"❌ {case_id}: HTTP {response.status_code}")
            failed += 1
            results.append({
                "case_id": case_id,
                "status": "FAILED",
                "reason": f"HTTP {response.status_code}"
            })
            continue
            
        actual = response.json()
        
        # Critical field checks
        checks = {
            "ticket_id": actual.get("ticket_id") == expected["ticket_id"],
            "relevant_transaction_id": actual.get("relevant_transaction_id") == expected["relevant_transaction_id"],
            "evidence_verdict": actual.get("evidence_verdict") == expected["evidence_verdict"],
            "case_type": actual.get("case_type") == expected["case_type"],
            "department": actual.get("department") == expected["department"],
            "severity": actual.get("severity") == expected["severity"],
            "human_review_required": actual.get("human_review_required") == expected["human_review_required"]
        }
        
        if all(checks.values()):
            print(f"✅ {case_id}: {case_label}")
            passed += 1
            results.append({
                "case_id": case_id,
                "status": "PASSED",
                "actual": actual
            })
        else:
            print(f"⚠️  {case_id}: {case_label}")
            print(f"   Failed checks: {[k for k, v in checks.items() if not v]}")
            failed += 1
            results.append({
                "case_id": case_id,
                "status": "PARTIAL",
                "failed_fields": [k for k, v in checks.items() if not v],
                "expected": expected,
                "actual": actual
            })
            
    except Exception as e:
        print(f"❌ {case_id}: Exception - {str(e)}")
        failed += 1
        results.append({
            "case_id": case_id,
            "status": "ERROR",
            "error": str(e)
        })

print(f"\n{'='*60}")
print(f"Results: {passed} passed, {failed} failed out of 10 cases")
print(f"{'='*60}\n")

# Save results
with open("sample_cases_test_results.json", "w") as f:
    json.dump(results, f, indent=2)
    
print("Detailed results saved to sample_cases_test_results.json")
sys.exit(0 if failed == 0 else 1)
