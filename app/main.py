from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.schemas import AnalyzeTicketRequest, AnalyzeTicketResponse

app = FastAPI(title="QueueStorm Investigator")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze-ticket")
def analyze_ticket(request: AnalyzeTicketRequest):
    # Dummy mock response to verify API plumbing works
    return {
        "ticket_id": request.ticket_id,
        "relevant_transaction_id": None,
        "evidence_verdict": "insufficient_data",
        "case_type": "other",
        "severity": "low",
        "department": "customer_support",
        "agent_summary": "Complaint received.",
        "recommended_next_action": "Wait for details.",
        "customer_reply": "Thank you. Please do not share PIN.",
        "human_review_required": False
    }
