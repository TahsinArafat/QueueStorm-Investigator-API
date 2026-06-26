"""
Unit tests for LLM Provider Pool with round-robin load balancing
"""

import os
import json
import pytest
import threading
from unittest.mock import Mock, patch, MagicMock
from concurrent.futures import ThreadPoolExecutor
from collections import Counter

from app.llm_provider import (
    LLMProviderConfig,
    LLMProviderPool,
    load_providers_from_env,
    get_provider_pool
)


class TestLLMProviderConfig:
    """Tests for LLMProviderConfig dataclass"""

    def test_config_creation(self):
        """Test creating a provider config"""
        config = LLMProviderConfig(
            name="test-provider",
            api_key="sk-test-key",
            base_url="https://api.test.com/v1",
            model="gpt-4o-mini",
            timeout=10.0
        )
        assert config.name == "test-provider"
        assert config.api_key == "sk-test-key"
        assert config.base_url == "https://api.test.com/v1"
        assert config.model == "gpt-4o-mini"
        assert config.timeout == 10.0

    def test_config_default_timeout(self):
        """Test default timeout value"""
        config = LLMProviderConfig(
            name="test",
            api_key="key",
            base_url="url",
            model="model"
        )
        assert config.timeout == 15.0


class TestLLMProviderPool:
    """Tests for LLMProviderPool class"""

    def test_pool_initialization(self):
        """Test pool initializes with providers"""
        providers = [
            LLMProviderConfig("p1", "key1", "url1", "model1"),
            LLMProviderConfig("p2", "key2", "url2", "model2"),
        ]
        pool = LLMProviderPool(providers)
        assert pool._providers == providers
        assert pool._counter == 0
        assert pool._clients == {}

    def test_pool_requires_providers(self):
        """Test pool raises error with empty provider list"""
        with pytest.raises(ValueError, match="At least one provider required"):
            LLMProviderPool([])

    def test_round_robin_rotation(self):
        """Test providers are rotated in round-robin order"""
        providers = [
            LLMProviderConfig("p1", "key1", "url1", "model1"),
            LLMProviderConfig("p2", "key2", "url2", "model2"),
            LLMProviderConfig("p3", "key3", "url3", "model3"),
        ]
        pool = LLMProviderPool(providers)

        # Mock OpenAI client creation
        with patch('app.llm_provider.OpenAI') as mock_openai:
            mock_openai.return_value = Mock()

            # Get 10 providers and check cycling
            names = [pool.get_next_provider()[0] for _ in range(10)]

        expected = ["p1", "p2", "p3", "p1", "p2", "p3", "p1", "p2", "p3", "p1"]
        assert names == expected

    def test_single_provider_rotation(self):
        """Test single provider is returned repeatedly"""
        providers = [LLMProviderConfig("only", "key", "url", "model")]
        pool = LLMProviderPool(providers)

        with patch('app.llm_provider.OpenAI') as mock_openai:
            mock_openai.return_value = Mock()
            names = [pool.get_next_provider()[0] for _ in range(5)]

        assert names == ["only", "only", "only", "only", "only"]

    def test_thread_safety(self):
        """Test concurrent access doesn't break rotation"""
        providers = [
            LLMProviderConfig(f"p{i}", f"key{i}", f"url{i}", "model")
            for i in range(3)
        ]
        pool = LLMProviderPool(providers)

        with patch('app.llm_provider.OpenAI') as mock_openai:
            mock_openai.return_value = Mock()

            def get_provider_name():
                return pool.get_next_provider()[0]

            # Run 100 requests across 10 threads
            with ThreadPoolExecutor(max_workers=10) as executor:
                results = list(executor.map(lambda _: get_provider_name(), range(100)))

        # Each provider should be called roughly 33-34 times (100/3)
        counts = Counter(results)
        assert len(counts) == 3
        for provider_name, count in counts.items():
            assert 30 <= count <= 37, f"Provider {provider_name} called {count} times (expected 30-37)"

    def test_client_caching(self):
        """Test OpenAI clients are cached and reused"""
        providers = [
            LLMProviderConfig("p1", "key1", "url1", "model1"),
            LLMProviderConfig("p2", "key2", "url2", "model2"),
        ]
        pool = LLMProviderPool(providers)

        with patch('app.llm_provider.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client

            # Get provider 1 twice
            name1, client1, _ = pool.get_next_provider()
            name2, client2, _ = pool.get_next_provider()
            name3, client3, _ = pool.get_next_provider()

            # OpenAI should only be called twice (once per unique provider)
            assert mock_openai.call_count == 2

            # Same provider should return same client instance
            assert client1 is client3  # Both are p1

    def test_should_retry_retriable_errors(self):
        """Test retriable errors are identified correctly"""
        pool = LLMProviderPool([LLMProviderConfig("p", "k", "u", "m")])

        # Rate limit errors
        assert pool.should_retry(Exception("rate_limit_exceeded")) is True
        assert pool.should_retry(Exception("Error 429: Too Many Requests")) is True

        # Timeout errors
        assert pool.should_retry(Exception("timeout occurred")) is True
        assert pool.should_retry(Exception("Request timed out")) is True
        assert pool.should_retry(Exception("Request timed out after 4000ms")) is True

        # Server errors
        assert pool.should_retry(Exception("503 Service Unavailable")) is True
        assert pool.should_retry(Exception("500 Internal Server Error")) is True

        # Connection errors
        assert pool.should_retry(Exception("Connection reset")) is True
        assert pool.should_retry(Exception("ConnectTimeout")) is True

    def test_should_retry_non_retriable_errors(self):
        """Test non-retriable errors are identified correctly"""
        pool = LLMProviderPool([LLMProviderConfig("p", "k", "u", "m")])

        # Authentication errors
        assert pool.should_retry(Exception("401 Unauthorized")) is False
        assert pool.should_retry(Exception("invalid_api_key")) is False

        # Bad request errors
        assert pool.should_retry(Exception("400 Bad Request")) is False
        assert pool.should_retry(Exception("invalid_request_error")) is False

        # Not found errors
        assert pool.should_retry(Exception("404 model_not_found")) is False

        import json
        json_error = json.JSONDecodeError("msg", "doc", 0)
        assert pool.should_retry(json_error) is False

    def test_should_retry_with_status_code(self):
        """Test error classification using status_code attribute"""
        pool = LLMProviderPool([LLMProviderConfig("p", "k", "u", "m")])

        # Mock exception with status_code attribute
        error_429 = Exception("Rate limited")
        error_429.status_code = 429
        assert pool.should_retry(error_429) is True

        error_500 = Exception("Server error")
        error_500.status_code = 500
        assert pool.should_retry(error_500) is True

        error_401 = Exception("Auth failed")
        error_401.status_code = 401
        assert pool.should_retry(error_401) is False

        error_400 = Exception("Bad request")
        error_400.status_code = 400
        assert pool.should_retry(error_400) is False

    def test_call_with_failover_success_first_try(self):
        """Test successful call on first provider"""
        providers = [
            LLMProviderConfig("p1", "key1", "url1", "model1"),
            LLMProviderConfig("p2", "key2", "url2", "model2"),
        ]
        pool = LLMProviderPool(providers)

        with patch('app.llm_provider.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client

            # Mock function that succeeds
            def mock_func(client, config):
                return {"result": "success"}

            result = pool.call_with_failover(mock_func, context="test")

        assert result == {"result": "success"}

    def test_call_with_failover_success_after_failure(self):
        """Test failover to second provider after first fails"""
        providers = [
            LLMProviderConfig("p1", "key1", "url1", "model1"),
            LLMProviderConfig("p2", "key2", "url2", "model2"),
            LLMProviderConfig("p3", "key3", "url3", "model3"),
        ]
        pool = LLMProviderPool(providers)

        with patch('app.llm_provider.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client

            call_count = 0

            def mock_func(client, config):
                nonlocal call_count
                call_count += 1
                if call_count <= 2:
                    # First two calls fail with rate limit
                    raise Exception("429 rate_limit_exceeded")
                return {"result": "success"}

            result = pool.call_with_failover(mock_func, context="test")

        assert result == {"result": "success"}
        assert call_count == 3  # Failed twice, succeeded third time

    def test_call_with_failover_all_fail(self):
        """Test all providers fail"""
        providers = [
            LLMProviderConfig("p1", "key1", "url1", "model1"),
            LLMProviderConfig("p2", "key2", "url2", "model2"),
        ]
        pool = LLMProviderPool(providers)

        with patch('app.llm_provider.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client

            def mock_func(client, config):
                raise Exception("timeout")

            with pytest.raises(Exception, match="timeout"):
                pool.call_with_failover(mock_func, context="test")

    def test_call_with_failover_non_retriable_stops_early(self):
        """Test non-retriable error stops failover immediately"""
        providers = [
            LLMProviderConfig("p1", "key1", "url1", "model1"),
            LLMProviderConfig("p2", "key2", "url2", "model2"),
            LLMProviderConfig("p3", "key3", "url3", "model3"),
        ]
        pool = LLMProviderPool(providers)

        with patch('app.llm_provider.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client

            call_count = 0

            def mock_func(client, config):
                nonlocal call_count
                call_count += 1
                raise Exception("401 invalid_api_key")

            with pytest.raises(Exception, match="401 invalid_api_key"):
                pool.call_with_failover(mock_func, context="test")

        # Should only try once (non-retriable error)
        assert call_count == 1


class TestLoadProvidersFromEnv:
    """Tests for loading providers from environment variables"""

    def test_load_from_llm_providers_json(self):
        """Test loading from LLM_PROVIDERS JSON format"""
        providers_json = json.dumps([
            {
                "name": "provider-1",
                "api_key": "sk-test-1",
                "base_url": "https://api1.com/v1",
                "model": "gpt-4o-mini",
                "timeout": 10
            },
            {
                "name": "provider-2",
                "api_key": "sk-test-2",
                "base_url": "https://api2.com/v1",
                "model": "gpt-4o",
                "timeout": 20
            }
        ])

        with patch.dict(os.environ, {"LLM_PROVIDERS": providers_json}, clear=True):
            providers = load_providers_from_env()

        assert len(providers) == 2
        assert providers[0].name == "provider-1"
        assert providers[0].api_key == "sk-test-1"
        assert providers[0].base_url == "https://api1.com/v1"
        assert providers[0].model == "gpt-4o-mini"
        assert providers[0].timeout == 10.0

        assert providers[1].name == "provider-2"
        assert providers[1].api_key == "sk-test-2"
        assert providers[1].timeout == 20.0

    def test_load_from_llm_providers_with_defaults(self):
        """Test loading with default values for optional fields"""
        providers_json = json.dumps([
            {
                "api_key": "sk-test",
            }
        ])

        with patch.dict(os.environ, {"LLM_PROVIDERS": providers_json}, clear=True):
            providers = load_providers_from_env()

        assert len(providers) == 1
        assert providers[0].name == "provider-0"  # Default name
        assert providers[0].base_url == "https://api.openai.com/v1"  # Default
        assert providers[0].model == "gpt-4o-mini"  # Default
        assert providers[0].timeout == 15.0  # Default

    def test_load_from_legacy_format(self):
        """Test loading from legacy OPENAI_API_KEY format"""
        env_vars = {
            "OPENAI_API_KEY": "sk-legacy-key",
            "OPENAI_API_BASE": "https://api.legacy.com/v1",
            "MODEL_NAME": "gpt-4o"
        }

        with patch.dict(os.environ, env_vars, clear=True):
            providers = load_providers_from_env()

        assert len(providers) == 1
        assert providers[0].name == "default"
        assert providers[0].api_key == "sk-legacy-key"
        assert providers[0].base_url == "https://api.legacy.com/v1"
        assert providers[0].model == "gpt-4o"
        assert providers[0].timeout == 15.0

    def test_load_from_legacy_format_with_defaults(self):
        """Test legacy format with default base_url and model"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-key"}, clear=True):
            providers = load_providers_from_env()

        assert len(providers) == 1
        assert providers[0].base_url == "https://api.openai.com/v1"
        assert providers[0].model == "gpt-4o-mini"

    def test_load_no_configuration(self):
        """Test with no configuration returns empty list"""
        with patch.dict(os.environ, {}, clear=True):
            providers = load_providers_from_env()

        assert providers == []

    def test_llm_providers_takes_precedence(self):
        """Test LLM_PROVIDERS takes precedence over legacy format"""
        providers_json = json.dumps([{"name": "new", "api_key": "sk-new"}])
        env_vars = {
            "LLM_PROVIDERS": providers_json,
            "OPENAI_API_KEY": "sk-legacy"
        }

        with patch.dict(os.environ, env_vars, clear=True):
            providers = load_providers_from_env()

        assert len(providers) == 1
        assert providers[0].name == "new"
        assert providers[0].api_key == "sk-new"

    def test_invalid_json_falls_back_to_legacy(self):
        """Test invalid JSON in LLM_PROVIDERS falls back to legacy"""
        env_vars = {
            "LLM_PROVIDERS": "not valid json",
            "OPENAI_API_KEY": "sk-legacy"
        }

        with patch.dict(os.environ, env_vars, clear=True):
            providers = load_providers_from_env()

        assert len(providers) == 1
        assert providers[0].api_key == "sk-legacy"

    def test_llm_providers_not_array(self):
        """Test LLM_PROVIDERS not an array falls back to legacy"""
        env_vars = {
            "LLM_PROVIDERS": '{"name": "test"}',  # Object, not array
            "OPENAI_API_KEY": "sk-legacy"
        }

        with patch.dict(os.environ, env_vars, clear=True):
            providers = load_providers_from_env()

        assert len(providers) == 1
        assert providers[0].api_key == "sk-legacy"

    def test_llm_providers_missing_required_field(self):
        """Test provider missing api_key is skipped"""
        providers_json = json.dumps([
            {"name": "valid", "api_key": "sk-test"},
            {"name": "invalid"},  # Missing api_key
        ])

        with patch.dict(os.environ, {"LLM_PROVIDERS": providers_json}, clear=True):
            providers = load_providers_from_env()

        # Should only load the valid provider
        assert len(providers) == 1
        assert providers[0].name == "valid"


class TestGetProviderPool:
    """Tests for get_provider_pool singleton function"""

    def test_get_provider_pool_creates_pool(self):
        """Test get_provider_pool creates a pool when providers configured"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test"}, clear=True):
            # Reset global pool
            import app.llm_provider
            app.llm_provider._provider_pool = None

            pool = get_provider_pool()

        assert pool is not None
        assert isinstance(pool, LLMProviderPool)

    def test_get_provider_pool_returns_none_no_config(self):
        """Test get_provider_pool returns None when no config"""
        with patch.dict(os.environ, {}, clear=True):
            # Reset global pool
            import app.llm_provider
            app.llm_provider._provider_pool = None

            pool = get_provider_pool()

        assert pool is None

    def test_get_provider_pool_singleton(self):
        """Test get_provider_pool returns same instance (singleton)"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test"}, clear=True):
            # Reset global pool
            import app.llm_provider
            app.llm_provider._provider_pool = None

            pool1 = get_provider_pool()
            pool2 = get_provider_pool()

        assert pool1 is pool2
