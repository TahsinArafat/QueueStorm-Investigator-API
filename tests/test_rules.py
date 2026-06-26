from app.rules import match_transaction, classify_ticket
from app.schemas import AnalyzeTicketRequest, TransactionHistoryEntry, EvidenceVerdictEnum, CaseTypeEnum, SeverityEnum, DepartmentEnum

def test_bangla_digit_normalization():
    from app.rules import normalize_bangla_digits
    assert normalize_bangla_digits("আমি ২০০০ টাকা ক্যাশ ইন করেছি") == "আমি 2000 টাকা ক্যাশ ইন করেছি"
    assert normalize_bangla_digits("৳৫০০০.৫০ টাকা") == "৳5000.50 টাকা"

def test_transaction_amount_matching():
    history = [
        TransactionHistoryEntry(
            transaction_id="TXN-01", timestamp="2026-04-14T12:00:00Z",
            type="transfer", amount=5000.0, counterparty="+8801712345678", status="completed"
        ),
        TransactionHistoryEntry(
            transaction_id="TXN-02", timestamp="2026-04-14T12:05:00Z",
            type="cash_in", amount=2000.0, counterparty="AGENT-01", status="pending"
        )
    ]
    
    # Matching 5000 BDT
    tx_id, verdict = match_transaction("I sent 5000 taka to wrong number", history)
    assert tx_id == "TXN-01"
    assert verdict == "consistent"

    # Matching pending cash-in of 2000
    tx_id, verdict = match_transaction("আমি ২০০০ টাকা ক্যাশইন করেছি কিন্তু পাইনি", history)
    assert tx_id == "TXN-02"
    assert verdict == "consistent"

def test_duplicate_payment_detection():
    history = [
        TransactionHistoryEntry(
            transaction_id="TXN-10001", timestamp="2026-04-14T08:15:30Z",
            type="payment", amount=850, counterparty="BILLER-DESCO", status="completed"
        ),
        TransactionHistoryEntry(
            transaction_id="TXN-10002", timestamp="2026-04-14T08:15:42Z",
            type="payment", amount=850, counterparty="BILLER-DESCO", status="completed"
        )
    ]
    tx_id, verdict = match_transaction("I paid my electricity bill 850 taka but it deducted twice", history)
    # The duplicate match logic must match the second transaction chronologically
    assert tx_id == "TXN-10002"
    assert verdict == "consistent"

def test_established_recipient_inconsistent():
    history = [
        TransactionHistoryEntry(
            transaction_id="TXN-9202", timestamp="2026-04-14T11:30:00Z",
            type="transfer", amount=2000, counterparty="+8801812345678", status="completed"
        ),
        TransactionHistoryEntry(
            transaction_id="TXN-9180", timestamp="2026-04-10T09:15:00Z",
            type="transfer", amount=2500, counterparty="+8801812345678", status="completed"
        ),
        TransactionHistoryEntry(
            transaction_id="TXN-9145", timestamp="2026-04-05T17:45:00Z",
            type="transfer", amount=1500, counterparty="+8801812345678", status="completed"
        )
    ]
    tx_id, verdict = match_transaction("I sent 2000 to the wrong person by mistake. Please reverse it.", history)
    assert tx_id == "TXN-9202"
    assert verdict == "inconsistent"
