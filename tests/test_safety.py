from app.safety import enforce_safety_guard

def test_credential_leak_scrubbing():
    # If the text asks for PIN/OTP
    reply = "Please share your PIN to verify your identity."
    scrubbed = enforce_safety_guard(reply, is_bangla=False)
    assert "never ask for your PIN" in scrubbed
    assert "share your PIN" not in scrubbed

def test_unauthorized_refund_promise():
    reply = "We will refund your 500 taka."
    scrubbed = enforce_safety_guard(reply, is_bangla=False)
    assert "eligible amount" in scrubbed
    assert "will refund" not in scrubbed
