import pytest
from unittest.mock import patch
from app.llm import get_fallback_texts

@pytest.fixture(autouse=True)
def mock_llm_generation():
    def mock_generate(*args, **kwargs):
        complaint = args[0] if len(args) > 0 else kwargs.get("complaint", "")
        ticket_id = args[1] if len(args) > 1 else kwargs.get("ticket_id", "")
        relevant_tx_id = args[2] if len(args) > 2 else kwargs.get("relevant_transaction_id")
        verdict = args[3] if len(args) > 3 else kwargs.get("evidence_verdict")
        case_type = args[4] if len(args) > 4 else kwargs.get("case_type")
        language = args[7] if len(args) > 7 else kwargs.get("language")
        
        return get_fallback_texts(
            ticket_id=ticket_id,
            case_type=case_type,
            verdict=verdict,
            relevant_tx_id=relevant_tx_id,
            language=language,
            complaint=complaint
        )
        
    with patch("app.main.generate_ticket_texts", side_effect=mock_generate) as mock:
        yield mock
