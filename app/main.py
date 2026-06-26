from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import dotenv
dotenv.load_dotenv()

from app.schemas import AnalyzeTicketRequest, AnalyzeTicketResponse, LanguageEnum
from app.rules import match_transaction, classify_ticket
from app.llm import generate_ticket_texts
from app.safety import enforce_safety_guard
from app.language_detector import detect_language

app = FastAPI(title="QueueStorm Investigator")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("app/static/index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze-ticket", response_model=AnalyzeTicketResponse)
def analyze_ticket(request: AnalyzeTicketRequest):
    client_lang = request.language
    if not client_lang:
        client_lang = detect_language(request.complaint, method="hybrid")

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
