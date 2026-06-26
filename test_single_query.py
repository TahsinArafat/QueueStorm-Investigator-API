import httpx
import time
import json

test_input = {
    "ticket_id": "TEST-TIMING",
    "complaint": "I sent 5000 taka to wrong number",
    "transaction_history": [
        {
            "transaction_id": "TXN-9101",
            "timestamp": "2026-04-14T14:08:22Z",
            "type": "transfer",
            "amount": 5000,
            "counterparty": "+8801719876543",
            "status": "completed"
        }
    ]
}

print("Sending single test query to measure response time...")
start = time.time()

try:
    response = httpx.post(
        "http://127.0.0.1:8000/analyze-ticket",
        json=test_input,
        timeout=30.0
    )
    elapsed = time.time() - start
    
    print(f"\n✅ Response received!")
    print(f"⏱️  Time taken: {elapsed:.2f} seconds")
    print(f"📊 HTTP Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nResponse preview:")
        print(f"  case_type: {result['case_type']}")
        print(f"  evidence_verdict: {result['evidence_verdict']}")
        print(f"  department: {result['department']}")
        print(f"  relevant_transaction_id: {result['relevant_transaction_id']}")
        
except httpx.TimeoutException:
    elapsed = time.time() - start
    print(f"\n❌ Request TIMED OUT after {elapsed:.2f} seconds")
    
except Exception as e:
    elapsed = time.time() - start
    print(f"\n❌ Error after {elapsed:.2f} seconds: {e}")

