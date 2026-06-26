import httpx
import json

print("Testing Edge Cases and Robustness\n" + "="*70)

edge_tests = [
    {
        "name": "Malformed JSON",
        "input": '{"ticket_id": "TEST", "complaint": "test", invalid json',
        "expected_status": 400,
        "is_json": False
    },
    {
        "name": "Missing Required Field (complaint)",
        "input": {"ticket_id": "TEST-001"},
        "expected_status": 422,
        "is_json": True
    },
    {
        "name": "Empty Complaint String",
        "input": {"ticket_id": "TEST-002", "complaint": ""},
        "expected_status": [200, 422],  # Either is acceptable
        "is_json": True
    },
    {
        "name": "Very Long Complaint (1000+ chars)",
        "input": {
            "ticket_id": "TEST-003",
            "complaint": "A" * 1500 + " I need help",
            "transaction_history": []
        },
        "expected_status": 200,
        "is_json": True
    },
    {
        "name": "Empty Transaction History",
        "input": {
            "ticket_id": "TEST-004",
            "complaint": "I sent money but it failed",
            "transaction_history": []
        },
        "expected_status": 200,
        "is_json": True
    },
    {
        "name": "Unicode Characters (Emoji)",
        "input": {
            "ticket_id": "TEST-005",
            "complaint": "আমার টাকা 😢 ফেরত চাই 💰",
            "transaction_history": []
        },
        "expected_status": 200,
        "is_json": True
    }
]

passed = 0
failed = 0

for test in edge_tests:
    print(f"\n{test['name']}")
    try:
        if test["is_json"]:
            response = httpx.post(
                "http://127.0.0.1:8000/analyze-ticket",
                json=test["input"],
                timeout=30.0
            )
        else:
            response = httpx.post(
                "http://127.0.0.1:8000/analyze-ticket",
                content=test["input"],
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )
        
        expected = test["expected_status"]
        if isinstance(expected, list):
            status_ok = response.status_code in expected
        else:
            status_ok = response.status_code == expected
        
        if status_ok:
            print(f"  ✅ PASS - Status {response.status_code}")
            passed += 1
        else:
            print(f"  ❌ FAIL - Expected {expected}, got {response.status_code}")
            failed += 1
            
    except Exception as e:
        print(f"  ❌ ERROR: {str(e)[:80]}")
        failed += 1

print("\n" + "="*70)
print(f"Edge Case Tests: {passed} passed, {failed} failed (out of {len(edge_tests)})")
print("="*70)

