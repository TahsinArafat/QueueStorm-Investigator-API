"""
Integration test for round-robin multi-provider setup
Run this manually to verify the round-robin behavior with real/mock API calls
"""

import os
import json
from app.llm import generate_ticket_texts
from app.schemas import (
    CaseTypeEnum,
    EvidenceVerdictEnum,
    LanguageEnum,
    SeverityEnum,
    DepartmentEnum
)


def test_single_provider_legacy_format():
    """Test backwards compatibility with single provider"""
    print("\n=== Test 1: Single Provider (Legacy Format) ===")

    # Set legacy environment variables
    os.environ["OPENAI_API_KEY"] = "sk-test-key"
    os.environ["OPENAI_API_BASE"] = "https://api.openai.com/v1"
    os.environ["MODEL_NAME"] = "gpt-4o-mini"
    os.environ.pop("LLM_PROVIDERS", None)

    # Reset provider pool
    import app.llm_provider
    app.llm_provider._provider_pool = None

    # Make a test call (will use fallback since no real API key)
    result = generate_ticket_texts(
        complaint="Test complaint",
        ticket_id="TEST-001",
        relevant_transaction_id="TXN-123",
        evidence_verdict=EvidenceVerdictEnum.consistent,
        case_type=CaseTypeEnum.wrong_transfer,
        severity=SeverityEnum.high,
        department=DepartmentEnum.dispute_resolution,
        language=LanguageEnum.en
    )

    print(f"✓ Single provider works (used fallback)")
    print(f"  Agent Summary: {result['agent_summary'][:80]}...")
    assert "agent_summary" in result
    assert "customer_reply" in result
    assert "recommended_next_action" in result


def test_multiple_providers_json_format():
    """Test multiple providers in JSON format"""
    print("\n=== Test 2: Multiple Providers (JSON Format) ===")

    # Set multi-provider configuration
    providers = [
        {
            "name": "provider-1",
            "api_key": "sk-test-key-1",
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4o-mini",
            "timeout": 15
        },
        {
            "name": "provider-2",
            "api_key": "sk-test-key-2",
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4o-mini",
            "timeout": 15
        },
        {
            "name": "provider-3",
            "api_key": "sk-test-key-3",
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4o-mini",
            "timeout": 15
        }
    ]

    os.environ["LLM_PROVIDERS"] = json.dumps(providers)
    os.environ.pop("OPENAI_API_KEY", None)

    # Reset provider pool
    import app.llm_provider
    app.llm_provider._provider_pool = None

    # Verify providers loaded
    from app.llm_provider import get_provider_pool
    pool = get_provider_pool()

    print(f"✓ Loaded {len(pool._providers)} providers")
    for p in pool._providers:
        print(f"  - {p.name}: {p.model} @ {p.base_url}")

    # Make multiple calls (will use fallback but rotate through providers)
    for i in range(5):
        result = generate_ticket_texts(
            complaint=f"Test complaint {i+1}",
            ticket_id=f"TEST-{i+1:03d}",
            relevant_transaction_id="TXN-123",
            evidence_verdict=EvidenceVerdictEnum.consistent,
            case_type=CaseTypeEnum.payment_failed,
            severity=SeverityEnum.medium,
            department=DepartmentEnum.customer_support,
            language=LanguageEnum.en
        )
        assert "agent_summary" in result

    print(f"✓ Made 5 requests with round-robin rotation")


def test_provider_pool_rotation():
    """Test that provider pool actually rotates"""
    print("\n=== Test 3: Verify Round-Robin Rotation ===")

    from app.llm_provider import LLMProviderConfig, LLMProviderPool
    from unittest.mock import Mock, patch

    providers = [
        LLMProviderConfig("p1", "key1", "url1", "model1"),
        LLMProviderConfig("p2", "key2", "url2", "model2"),
        LLMProviderConfig("p3", "key3", "url3", "model3"),
    ]
    pool = LLMProviderPool(providers)

    # Mock OpenAI client
    with patch('app.llm_provider.OpenAI') as mock_openai:
        mock_openai.return_value = Mock()

        # Get providers and check rotation
        names = [pool.get_next_provider()[0] for _ in range(9)]

    expected = ["p1", "p2", "p3", "p1", "p2", "p3", "p1", "p2", "p3"]

    print(f"✓ Rotation order: {names}")
    assert names == expected, f"Expected {expected}, got {names}"


if __name__ == "__main__":
    print("=" * 70)
    print("Round-Robin Multi-Provider Integration Tests")
    print("=" * 70)

    try:
        test_single_provider_legacy_format()
        test_multiple_providers_json_format()
        test_provider_pool_rotation()

        print("\n" + "=" * 70)
        print("✓ ALL TESTS PASSED")
        print("=" * 70)

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
