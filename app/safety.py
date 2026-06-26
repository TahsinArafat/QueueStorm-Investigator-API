import re

SAFE_REPLY_EN = (
    "We have received your concern. Please note that we never ask for your PIN, OTP, or password. "
    "Our support team will review the case and contact you shortly through official channels."
)

SAFE_REPLY_BN = (
    "আমরা আপনার অভিযোগটি পেয়েছি। অনুগ্রহ করে মনে রাখবেন যে আমরা কখনই আপনার পিন, ওটিপি বা পাসওয়ার্ড জানতে চাই না। "
    "আমাদের সাপোর্ট টিম বিষয়টি পর্যালোচনা করে দ্রুত অফিশিয়াল চ্যানেলে আপনার সাথে যোগাযোগ করবে।"
)

def enforce_safety_guard(text: str, is_bangla: bool = False) -> str:
    text = text.replace('\u2011', '-').replace('\u2012', '-').replace('\u2013', '-').replace('\u2014', '-').replace('\u2015', '-')
    lower_text = text.lower()
    
    # 1. Credentials warning and request checker
    cred_keywords = ["pin", "otp", "password", "passcode", "cvv", "card number", "পিন", "ওটিপি", "পাসওয়ার্ড", "পাসকোড"]
    has_cred = any(kw in lower_text for kw in cred_keywords)
    
    is_unsafe_request = False
    if has_cred:
        unsafe_verbs = ["share", "send", "tell", "give", "write", "provide", "input", "type", "enter", "verify", "পাঠান", "দিন", "বলুন", "লিখুন", "টাইপ"]
        verbs_found = [v for v in unsafe_verbs if v in lower_text]
        if verbs_found:
            warning_indicators = [
                "do not", "don't", "dont", "never", "no one", "not share", "should not", "must not",
                "করবেন না", "শেয়ার করবেন না", "দেবেন না", "না", "নিরাপদ রাখুন"
            ]
            is_warning = any(wi in lower_text for wi in warning_indicators)
            if not is_warning:
                is_unsafe_request = True

    # 16 digit card number check
    if re.search(r'\b\d{16}\b', text):
        is_unsafe_request = True

    if is_unsafe_request:
        return SAFE_REPLY_BN if is_bangla else SAFE_REPLY_EN

    # 2. Refund promise scrub
    # Matches strings that guarantee reversal or cash return
    refund_promises = [
        (r'\b(?:we will refund|we reverse|refunded|reversed|refund your money|money back|we will revert|reversed your transaction)\b', "any eligible amount will be returned through official channels"),
        (r'(?:ফেরত দেব|রিফান্ড করব|ফেরত দেওয়া হবে|টাকা ফেরত পাবেন)', "আপনার কোনো প্রাপ্য টাকা থাকলে তা অফিসিয়াল চ্যানেলের মাধ্যমে ফেরত দেওয়া হবে।")
    ]
    
    scrubbed = text
    for pattern, replacement in refund_promises:
        scrubbed = re.sub(pattern, replacement, scrubbed, flags=re.IGNORECASE)

    # 3. Restrict external support third-parties
    # Remove direct URLs or external phone numbers
    scrubbed = re.sub(r'https?://[^\s]+', "[official support]", scrubbed)
    scrubbed = re.sub(r'\b01[1-9]\d{8}\b', "[official hotline]", scrubbed)

    return scrubbed
