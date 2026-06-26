import json
import httpx

# Test just the first 3 sample cases quickly
with open("Preliminary Questions and Resources/SUST_Preli_Sample_Cases.json") as f:
    data = json.load(f)

for i, case in enumerate(data["cases"][:3]):
    case_id = case["id"]
    input_data = case["input"]
    expected = case["expected_output"]
    
    print(f"\n{'='*60}")
    print(f"Testing {case_id}: {case['label']}")
    print(f"{'='*60}")
    
    try:
        response = httpx.post(
            "http://127.0.0.1:8000/analyze-ticket",
            json=input_data,
            timeout=10.0
        )
        
        actual = response.json()
        
        print(f"Expected: {expected['case_type']} -> {expected['department']} (verdict: {expected['evidence_verdict']})")
        print(f"Actual:   {actual['case_type']} -> {actual['department']} (verdict: {actual['evidence_verdict']})")
        
        match = (
            actual['case_type'] == expected['case_type'] and
            actual['department'] == expected['department'] and
            actual['evidence_verdict'] == expected['evidence_verdict'] and
            actual['relevant_transaction_id'] == expected['relevant_transaction_id']
        )
        
        print(f"Status: {'✅ PASS' if match else '❌ FAIL'}")
        
        if not match:
            print("\nDifferences:")
            for key in ['case_type', 'department', 'evidence_verdict', 'relevant_transaction_id']:
                if actual.get(key) != expected.get(key):
                    print(f"  {key}: expected '{expected.get(key)}', got '{actual.get(key)}'")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

