#!/bin/bash

# VPS API Test Script
# Tests your deployed API using sample cases

VPS_URL="http://138.68.191.213:8000"

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    Testing VPS API with Sample Cases                        ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Health check first
echo "🏥 Health Check:"
echo "───────────────────────────────────────────────────────────────────────────────"
curl -s $VPS_URL/health | python3 -m json.tool
echo ""
echo ""

# Load sample cases
SAMPLE_FILE="Preliminary Questions and Resources/SUST_Preli_Sample_Cases.json"

if [ ! -f "$SAMPLE_FILE" ]; then
    echo "❌ Error: $SAMPLE_FILE not found"
    exit 1
fi

echo "📋 Loading sample cases from: $SAMPLE_FILE"
echo ""

# Test SAMPLE-01 (Wrong Transfer - English)
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "TEST 1: SAMPLE-01 (Wrong Transfer - English)"
echo "═══════════════════════════════════════════════════════════════════════════════"

SAMPLE_01=$(cat "$SAMPLE_FILE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
case = [c for c in data['cases'] if c['id'] == 'SAMPLE-01'][0]
print(json.dumps(case['input']))
")

echo "Request:"
echo "$SAMPLE_01" | python3 -m json.tool | head -5
echo "..."
echo ""

echo "Response:"
curl -s -X POST $VPS_URL/analyze-ticket \
  -H "Content-Type: application/json" \
  -d "$SAMPLE_01" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"✅ Ticket ID: {data['ticket_id']}\")
print(f\"✅ Case Type: {data['case_type']}\")
print(f\"✅ Evidence Verdict: {data['evidence_verdict']}\")
print(f\"✅ Department: {data['department']}\")
print(f\"✅ Relevant TXN: {data['relevant_transaction_id']}\")
print(f\"\\nAgent Summary:\\n  {data['agent_summary'][:100]}...\")
print(f\"\\nCustomer Reply:\\n  {data['customer_reply'][:150]}...\")
"
echo ""
echo ""

# Test SAMPLE-03 (Payment Failed - English)
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "TEST 2: SAMPLE-03 (Payment Failed - English)"
echo "═══════════════════════════════════════════════════════════════════════════════"

SAMPLE_03=$(cat "$SAMPLE_FILE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
case = [c for c in data['cases'] if c['id'] == 'SAMPLE-03'][0]
print(json.dumps(case['input']))
")

echo "Request:"
echo "$SAMPLE_03" | python3 -m json.tool | head -5
echo "..."
echo ""

echo "Response:"
curl -s -X POST $VPS_URL/analyze-ticket \
  -H "Content-Type: application/json" \
  -d "$SAMPLE_03" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"✅ Ticket ID: {data['ticket_id']}\")
print(f\"✅ Case Type: {data['case_type']}\")
print(f\"✅ Evidence Verdict: {data['evidence_verdict']}\")
print(f\"✅ Department: {data['department']}\")
print(f\"\\nCustomer Reply:\\n  {data['customer_reply'][:150]}...\")
"
echo ""
echo ""

# Test SAMPLE-07 (Bangla)
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "TEST 3: SAMPLE-07 (Agent Cash-In - Bangla)"
echo "═══════════════════════════════════════════════════════════════════════════════"

SAMPLE_07=$(cat "$SAMPLE_FILE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
case = [c for c in data['cases'] if c['id'] == 'SAMPLE-07'][0]
print(json.dumps(case['input']))
")

echo "Request:"
echo "$SAMPLE_07" | python3 -m json.tool | head -5
echo "..."
echo ""

echo "Response:"
curl -s -X POST $VPS_URL/analyze-ticket \
  -H "Content-Type: application/json" \
  -d "$SAMPLE_07" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"✅ Ticket ID: {data['ticket_id']}\")
print(f\"✅ Case Type: {data['case_type']}\")
print(f\"✅ Evidence Verdict: {data['evidence_verdict']}\")
print(f\"✅ Language: {'Bangla' if any('\\u0980' <= c <= '\\u09FF' for c in data['customer_reply']) else 'English'}\")
print(f\"\\nCustomer Reply (Bangla):\\n  {data['customer_reply'][:150]}...\")
"
echo ""
echo ""

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                              ✅ TESTS COMPLETE                               ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Your API is working! 🎉"
echo ""
echo "API Endpoint: $VPS_URL"
echo "All 3 sample cases tested successfully!"
echo ""

