import json
import httpx
import time

# Load sample cases
with open("Preliminary Questions and Resources/SUST_Preli_Sample_Cases.json") as f:
    data = json.load(f)

results = []
passed = 0
failed = 0
partial = 0

print("Testing all 10 sample cases...\n")
print("="*70)

for case in data["cases"]:
    case_id = case["id"]
    case_label = case["label"]
    input_data = case["input"]
    expected = case["expected_output"]
    
    print(f"\n{case_id}: {case_label}")
    
    start = time.time()
    try:
        response = httpx.post(
            "http://127.0.0.1:8000/analyze-ticket",
            json=input_data,
            timeout=30.0
        )
        elapsed = time.time() - start
        
        if response.status_code != 200:
            print(f"  ❌ HTTP {response.status_code} ({elapsed:.1f}s)")
            failed += 1
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
        
        failed_checks = [k for k, v in checks.items() if not v]
        
        if not failed_checks:
            print(f"  ✅ PASS ({elapsed:.1f}s)")
            passed += 1
            results.append({"case_id": case_id, "status": "PASSED", "time": elapsed, "output": actual})
        else:
            print(f"  ⚠️  PARTIAL ({elapsed:.1f}s) - Failed: {', '.join(failed_checks)}")
            partial += 1
            results.append({
                "case_id": case_id, 
                "status": "PARTIAL", 
                "failed_fields": failed_checks,
                "time": elapsed,
                "expected": {k: expected[k] for k in failed_checks},
                "actual": {k: actual.get(k) for k in failed_checks}
            })
            
    except httpx.TimeoutException:
        elapsed = time.time() - start
        print(f"  ❌ TIMEOUT ({elapsed:.1f}s)")
        failed += 1
    except Exception as e:
        elapsed = time.time() - start
        print(f"  ❌ ERROR ({elapsed:.1f}s): {str(e)[:50]}")
        failed += 1

print("\n" + "="*70)
print(f"RESULTS: {passed} passed, {partial} partial, {failed} failed (out of 10)")
print("="*70)

# Save detailed results
with open("comprehensive_test_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n✅ Detailed results saved to comprehensive_test_results.json")

