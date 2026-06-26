from fastapi import FastAPI, HTTPException
from app.schemas import AnalyzeTicketRequest, AnalyzeTicketResponse, LanguageEnum
from app.rules import match_transaction, classify_ticket, detect_bangla_chars
from app.llm import generate_ticket_texts
from app.safety import enforce_safety_guard

app = FastAPI(title="QueueStorm Investigator")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze-ticket", response_model=AnalyzeTicketResponse)
def analyze_ticket(request: AnalyzeTicketRequest):
    # 1. Determine Language natively if not supplied
    client_lang = request.language
    if not client_lang:
        client_lang = LanguageEnum.bn if detect_bangla_chars(request.complaint) else LanguageEnum.en

    # 2. Deterministic Rule Matching
    relevant_tx_id, verdict = match_transaction(
        request.complaint, request.transaction_history or []
    )
    
    # 3. Classification & Routing
    has_txn = relevant_tx_id is not None
    case_type, severity, department, human_review = classify_ticket(
        request.complaint, verdict, has_txn
    )
    
    # 4. LLM/Fallback Generation
    generated = generate_ticket_texts(
        complaint=request.complaint,
        ticket_id=request.ticket_id,
        relevant_transaction_id=relevant_tx_id,
        evidence_verdict=verdict,
        case_type=case_type,
        severity=severity,
        department=department,
        language=client_lang
    )
    
    # 5. Deterministic Safety Overrides
    is_bn = (client_lang == LanguageEnum.bn or client_lang == LanguageEnum.mixed)
    safe_reply = enforce_safety_guard(generated["customer_reply"], is_bn)
    safe_next_action = enforce_safety_guard(generated["recommended_next_action"], is_bn)
    
    # 6. Build final response
    return AnalyzeTicketResponse(
        ticket_id=request.ticket_id,
        relevant_transaction_id=relevant_tx_id,
        evidence_verdict=verdict,
        case_type=case_type,
        severity=severity,
        department=department,
        agent_summary=generated["agent_summary"],
        recommended_next_action=safe_next_action,
        customer_reply=safe_reply,
        human_review_required=human_review,
        confidence=0.9 if verdict == "consistent" else 0.7,
        reason_codes=[case_type.value, verdict.value]
    )
