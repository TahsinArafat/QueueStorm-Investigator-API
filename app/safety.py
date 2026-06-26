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
    # 1. Anti-Credential Protection Check
    # Match keywords asking or suggesting credentials
    cred_patterns = [
        r'\b(?:pin|otp|password|passcode|cvv|card\s*number)\b',
        r'(?:পিন|ওটিপি|পাসওয়ার্ড|পাসকোড)'
    ]
    
    # If LLM asks or mentions sensitive keywords contextually in an insecure way:
    # E.g. "enter your pin", "send us your otp"
    lower_text = text.lower()
    unsafe_keywords = ["share", "send", "tell", "give", "write", "provide", "পাঠান", "দিন", "শেয়ার", "বলুন", "input", "টাইপ"]
    
    has_cred = any(re.search(pattern, lower_text) for pattern in cred_patterns)
    is_unsafe_request = has_cred and any(ukw in lower_text for ukw in unsafe_keywords)
    
    # Explicitly check for card or pass numbers
    if is_unsafe_request or re.search(r'\b\d{16}\b', text):
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
