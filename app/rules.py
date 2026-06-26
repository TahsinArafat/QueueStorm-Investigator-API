import re
from datetime import datetime
from typing import List, Optional, Tuple
from app.schemas import (
    AnalyzeTicketRequest, TransactionHistoryEntry, EvidenceVerdictEnum,
    CaseTypeEnum, SeverityEnum, DepartmentEnum
)

BANGLA_DIGITS_MAP = {
    '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4',
    '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9'
}

def normalize_bangla_digits(text: str) -> str:
    for bn, en in BANGLA_DIGITS_MAP.items():
        text = text.replace(bn, en)
    return text

def parse_amounts(text: str) -> List[float]:
    normalized = normalize_bangla_digits(text)
    # Find numbers that represent money (including decimals)
    matches = re.findall(r'\b\d+(?:\.\d+)?\b', normalized)
    return [float(m) for m in matches]

def extract_counterparties(text: str) -> List[str]:
    # Extract phone numbers, agent IDs, biller IDs, etc.
    # Matches common phone patterns 01xxxxxxxxx or +8801xxxxxxxxx
    phones = re.findall(r'(?:\+?88)?01[3-9]\d{8}\b', text)
    # Matches AGENT-xxx or MERCHANT-xxx or BILLER-xxx
    others = re.findall(r'\b(?:AGENT|MERCHANT|BILLER)-\w+\b', text, re.IGNORECASE)
    return phones + [o.upper() for o in others]

def detect_bangla_chars(text: str) -> bool:
    # Match any character in the Bangla Unicode range
    return bool(re.search(r'[\u0980-\u09ff]', text))

def parse_iso_time(timestamp_str: str) -> datetime:
    try:
        return datetime.strptime(timestamp_str.replace("Z", "+00:00"), "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        return datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))

def match_transaction(complaint: str, history: List[TransactionHistoryEntry]) -> Tuple[Optional[str], EvidenceVerdictEnum]:
    if not history:
        return None, EvidenceVerdictEnum.insufficient_data

    amounts = parse_amounts(complaint)
    counterparties = extract_counterparties(complaint)

    # Detect duplicate payments first if complaints suggest duplicate
    is_duplicate_claim = any(kw in complaint.lower() for kw in ["twice", "double", "duplicate", "two times", "দুইবার", "২ বার", "ডাবল"])
    if is_duplicate_claim and len(history) >= 2:
        # Look for identical payments within short window
        for i in range(len(history)):
            t1 = history[i]
            for j in range(i + 1, len(history)):
                t2 = history[j]
                if t1.amount == t2.amount and t1.type == t2.type and t1.counterparty == t2.counterparty and t1.status == "completed" and t2.status == "completed":
                    # Check time difference (e.g. less than 10 minutes)
                    try:
                        time1 = parse_iso_time(t1.timestamp)
                        time2 = parse_iso_time(t2.timestamp)
                        if abs((time1 - time2).total_seconds()) < 600:
                            # Return the second transaction (duplicate)
                            second_tx = t1 if time1 > time2 else t2
                            return second_tx.transaction_id, EvidenceVerdictEnum.consistent
                    except Exception:
                        pass

    if not amounts:
        return None, EvidenceVerdictEnum.insufficient_data

    # Filter transactions matching parsed amounts
    matched_by_amount = [t for t in history if any(abs(t.amount - amt) < 0.01 for amt in amounts)]

    if not matched_by_amount:
        return None, EvidenceVerdictEnum.insufficient_data

    # If single amount match, proceed
    if len(matched_by_amount) == 1:
        txn = matched_by_amount[0]
        # Inconsistency pattern checks (e.g. established counterparty history for wrong transfer claim)
        if txn.type == "transfer" and any(w in complaint.lower() or "ভুল" in complaint for w in ["wrong", "ভুল"]):
            # Check how many transactions were successfully completed with this counterparty
            prior_txs = [t for t in history if t.counterparty == txn.counterparty and t.status == "completed"]
            if len(prior_txs) >= 2:
                # User claims wrong transfer to someone they send money to regularly
                return txn.transaction_id, EvidenceVerdictEnum.inconsistent
        
        return txn.transaction_id, EvidenceVerdictEnum.consistent

    # If multiple amount matches, try counterparty lookup
    if counterparties:
        matched_by_cp = []
        for t in matched_by_amount:
            cleaned_t_cp = t.counterparty.replace("+88", "")
            if any(cleaned_t_cp in cp or cp.replace("+88", "") in cleaned_t_cp for cp in counterparties):
                matched_by_cp.append(t)
        if len(matched_by_cp) == 1:
            return matched_by_cp[0].transaction_id, EvidenceVerdictEnum.consistent

    # Ambiguity
    return None, EvidenceVerdictEnum.insufficient_data

def classify_ticket(complaint: str, verdict: EvidenceVerdictEnum, has_txn: bool) -> Tuple[CaseTypeEnum, SeverityEnum, DepartmentEnum, bool]:
    text = complaint.lower()
    
    # Check phishing/social engineering first (highest priority)
    phishing_keywords = ["otp", "pin", "password", "credential", "security code", "bkash agent call", "ওটিপি", "পিন", "পাসওয়ার্ড", "পাসকোড"]
    if any(kw in text for kw in phishing_keywords) and any(x in text for x in ["ask", "call", "send", "share", "বলছে", "চাচ্ছে", "ফোন"]):
        return CaseTypeEnum.phishing_or_social_engineering, SeverityEnum.critical, DepartmentEnum.fraud_risk, True

    # Case: wrong transfer
    wrong_transfer_keywords = [
        "wrong number", "wrong transfer", "wrong person", "wrong recipient", "mistake", "brother", "friend",
        "ভুল নম্বর", "ভুল নাম্বার", "ভুল করে", "ভুল নম্বরে", "ভুল নাম্বারে", "ভুল ব্যক্তি", "অন্য নম্বরে", "অন্য নাম্বারে",
        "পায়নি", "পাঠালাম", "পাঠিয়েছি", "পাঠানো"
    ]
    is_wrong_transfer = False
    if any(kw in text for kw in wrong_transfer_keywords) and any(x in text for x in ["send", "sent", "transfer", "taka", "টাকা", "পাঠা", "দিয়েছি", "দিয়েছি"]):
        is_wrong_transfer = True
    elif any(kw in text for kw in ["wrong number", "wrong transfer", "wrong person", "wrong recipient", "mistake", "ভুল নম্বর", "ভুল নাম্বার", "ভুল করে"]):
        is_wrong_transfer = True

    if is_wrong_transfer:
        severity = SeverityEnum.high if verdict == EvidenceVerdictEnum.consistent else SeverityEnum.medium
        hr = (verdict != EvidenceVerdictEnum.insufficient_data)
        return CaseTypeEnum.wrong_transfer, severity, DepartmentEnum.dispute_resolution, hr

    # Case: agent cash in
    if any(kw in text for kw in ["agent", "cash in", "cash-in", "ক্যাশ ইন", "ক্যাশইন", "এজেন্ট"]):
        return CaseTypeEnum.agent_cash_in_issue, SeverityEnum.high, DepartmentEnum.agent_operations, True

    # Case: merchant settlement
    if any(kw in text for kw in ["settlement", "settle", "merchant sales", "সেটেলমেন্ট"]):
        return CaseTypeEnum.merchant_settlement_delay, SeverityEnum.medium, DepartmentEnum.merchant_operations, False

    # Case: duplicate payment
    if any(kw in text for kw in ["twice", "double", "duplicate", "two times", "দুইবার", "২ বার", "ডাবল"]):
        return CaseTypeEnum.duplicate_payment, SeverityEnum.high, DepartmentEnum.payments_ops, True

    # Case: payment failed / balance deducted
    if any(kw in text for kw in ["failed", "deducted", " কেটে", "ব্যর্থ", "ব্যালেন্স", "recharge", "রিচার্জ"]):
        hr = (verdict != EvidenceVerdictEnum.consistent)
        return CaseTypeEnum.payment_failed, SeverityEnum.high, DepartmentEnum.payments_ops, hr

    # Case: refund request
    if any(kw in text for kw in ["refund", "refund request", "ফেরত চাই", "রিফান্ড", "change of mind", "don't want"]):
        return CaseTypeEnum.refund_request, SeverityEnum.low, DepartmentEnum.customer_support, False

    return CaseTypeEnum.other, SeverityEnum.low, DepartmentEnum.customer_support, False
