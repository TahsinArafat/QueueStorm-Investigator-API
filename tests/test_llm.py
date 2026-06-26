from app.llm import generate_ticket_texts, get_fallback_texts
from app.schemas import CaseTypeEnum, EvidenceVerdictEnum, LanguageEnum

def test_fallback_templates():
    texts = get_fallback_texts(
        ticket_id="TKT-99",
        case_type=CaseTypeEnum.wrong_transfer,
        verdict=EvidenceVerdictEnum.consistent,
        relevant_tx_id="TXN-123",
        language=LanguageEnum.en
    )
    assert "TXN-123" in texts["customer_reply"]
    assert "dispute" in texts["recommended_next_action"].lower()
    # The template mentions PIN/OTP security warning
    assert "PIN" in texts["customer_reply"]
