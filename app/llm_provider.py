"""
LLM Provider Pool with Round-Robin Load Balancing and Automatic Failover

This module provides a thread-safe provider pool that distributes LLM requests
across multiple API endpoints/keys in round-robin fashion with automatic failover.
"""

import os
import json
import logging
import threading
from typing import List, Tuple, Callable, Any, Optional
from dataclasses import dataclass
from openai import OpenAI

logger = logging.getLogger(__name__)


@dataclass
class LLMProviderConfig:
    """Configuration for a single LLM provider"""
    name: str
    api_key: str
    base_url: str
    model: str
    timeout: float = 15.0


class LLMProviderPool:
    """
    Thread-safe round-robin pool of LLM providers with automatic failover.

    Distributes requests across multiple providers in round-robin order.
    On failure, automatically tries the next provider in rotation.
    Caches OpenAI client instances for connection reuse.
    """

    # Error patterns that should trigger failover to next provider
    RETRIABLE_ERROR_PATTERNS = [
        "rate_limit", "429", "timeout", "timed out",
        "503", "502", "500", "service_unavailable",
        "connection", "connecttimeout", "readtimeout"
    ]

    # Error patterns that should fail fast (won't be fixed by trying another provider)
    NON_RETRIABLE_ERROR_PATTERNS = [
        "401", "invalid_api_key",
        "400", "invalid_request",
        "404", "model_not_found"
    ]

    def __init__(self, providers: List[LLMProviderConfig]):
        """
        Initialize provider pool.

        Args:
            providers: List of provider configurations (must have at least one)

        Raises:
            ValueError: If providers list is empty
        """
        if not providers:
            raise ValueError("At least one provider required")

        self._providers = providers
        self._clients = {}  # Cache of OpenAI client instances
        self._lock = threading.Lock()
        self._counter = 0

        logger.info(f"Initialized LLM provider pool with {len(providers)} providers: {[p.name for p in providers]}")

    def get_next_provider(self) -> Tuple[str, OpenAI, LLMProviderConfig]:
        """
        Get next provider in round-robin order (thread-safe).

        Returns:
            Tuple of (provider_name, openai_client, provider_config)
        """
        # Thread-safe counter increment
        with self._lock:
            index = self._counter % len(self._providers)
            self._counter += 1

        config = self._providers[index]

        # Lazy-initialize and cache OpenAI client (thread-safe)
        if config.name not in self._clients:
            with self._lock:
                # Double-check locking pattern
                if config.name not in self._clients:
                    self._clients[config.name] = OpenAI(
                        api_key=config.api_key,
                        base_url=config.base_url
                    )
                    logger.debug(f"Created OpenAI client for provider: {config.name}")

        return config.name, self._clients[config.name], config

    def should_retry(self, error: Exception) -> bool:
        """
        Determine if error warrants trying next provider.

        Args:
            error: Exception that occurred during LLM call

        Returns:
            True if should try next provider, False if should fail fast
        """
        error_str = str(error).lower()

        # Check non-retriable patterns first (fail fast)
        if any(pattern in error_str for pattern in self.NON_RETRIABLE_ERROR_PATTERNS):
            return False

        # Check retriable patterns
        if any(pattern in error_str for pattern in self.RETRIABLE_ERROR_PATTERNS):
            return True

        # Check OpenAI exception status codes if available
        if hasattr(error, 'status_code'):
            if error.status_code == 429:  # Rate limit
                return True
            if error.status_code >= 500:  # Server errors
                return True
            if error.status_code in (400, 401, 404):  # Client errors
                return False

        # Default: retry for unknown errors
        return True

    def call_with_failover(
        self,
        func: Callable[[OpenAI, LLMProviderConfig], Any],
        context: str = ""
    ) -> Any:
        """
        Execute function with automatic failover across all providers.

        Tries each provider in round-robin order until one succeeds or all fail.

        Args:
            func: Function to execute, receives (client, config) as arguments
            context: Context string for logging (e.g., "ticket=TEST-001")

        Returns:
            Result from successful provider

        Raises:
            Exception: If all providers fail, raises the last exception
        """
        last_error = None

        for attempt in range(len(self._providers)):
            provider_name, client, config = self.get_next_provider()

            try:
                result = func(client, config)

                # Log success after failures
                if attempt > 0:
                    logger.info(
                        f"Provider '{provider_name}' succeeded after {attempt} failures ({context})"
                    )

                return result

            except Exception as e:
                last_error = e
                should_retry = self.should_retry(e)

                # Log failure with details
                error_type = type(e).__name__
                error_msg = str(e)[:100]  # Truncate long error messages
                logger.warning(
                    f"Provider '{provider_name}' failed (attempt {attempt + 1}/{len(self._providers)}): "
                    f"{error_type}: {error_msg} | Retry: {should_retry} ({context})"
                )

                # Stop trying if non-retriable error
                if not should_retry:
                    logger.info(f"Non-retriable error, stopping failover ({context})")
                    break

                # Log if this was the last provider
                if attempt == len(self._providers) - 1:
                    logger.error(f"All {len(self._providers)} providers exhausted ({context})")

        # All providers failed, raise the last error
        raise last_error if last_error else Exception("All providers failed")


def load_providers_from_env() -> List[LLMProviderConfig]:
    """
    Load provider configuration from environment variables.

    Supports two formats:
    1. New format: LLM_PROVIDERS='[{"name":"p1","api_key":"...","base_url":"...","model":"..."}]'
    2. Legacy format: OPENAI_API_KEY, OPENAI_API_BASE, MODEL_NAME

    Returns:
        List of provider configurations (may be empty if no config found)
    """

    # Try new multi-provider format first
    providers_json = os.environ.get("LLM_PROVIDERS")
    if providers_json:
        try:
            providers_data = json.loads(providers_json)

            if not isinstance(providers_data, list):
                logger.error("LLM_PROVIDERS must be a JSON array")
                # Fall through to legacy format
            else:
                providers = []
                for i, p in enumerate(providers_data):
                    try:
                        provider = LLMProviderConfig(
                            name=p.get("name", f"provider-{i}"),
                            api_key=p["api_key"],
                            base_url=p.get("base_url", "https://api.openai.com/v1"),
                            model=p.get("model", "gpt-4o-mini"),
                            timeout=float(p.get("timeout", 15.0))
                        )
                        providers.append(provider)
                    except (KeyError, ValueError) as e:
                        logger.error(f"Invalid provider config at index {i}: {e}")
                        continue

                if providers:
                    logger.info(f"Loaded {len(providers)} providers from LLM_PROVIDERS")
                    return providers
                else:
                    logger.warning("LLM_PROVIDERS contained no valid providers")
                    # Fall through to legacy format

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM_PROVIDERS JSON: {e}")
            # Fall through to legacy format

    # Fall back to legacy single-provider format
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        provider = LLMProviderConfig(
            name="default",
            api_key=api_key,
            base_url=os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1"),
            model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
            timeout=15.0
        )
        logger.info(f"Loaded single provider from legacy OPENAI_API_KEY format")
        return [provider]

    # No configuration found
    logger.warning("No LLM provider configuration found (neither LLM_PROVIDERS nor OPENAI_API_KEY)")
    return []


# Global singleton pool (initialized once at module load)
_provider_pool: Optional[LLMProviderPool] = None


def get_provider_pool() -> Optional[LLMProviderPool]:
    """
    Get or create the global provider pool.

    Returns:
        Provider pool instance, or None if no providers configured
    """
    global _provider_pool

    if _provider_pool is None:
        providers = load_providers_from_env()
        if providers:
            _provider_pool = LLMProviderPool(providers)

    return _provider_pool
