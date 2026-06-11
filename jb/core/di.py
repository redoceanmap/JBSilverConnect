from __future__ import annotations

from functools import lru_cache

from jb.core.account.mock_account_query import MockAccountQuery
from jb.core.config import settings
from jb.core.customer.mock_customer_directory import MockCustomerDirectory
from jb.core.llm.fallback_llm_adapter import FallbackLlmAdapter
from jb.core.llm.gemini_adapter import GeminiAdapter
from jb.core.llm.groq_adapter import GroqAdapter
from jb.core.llm.mock_llm_adapter import MockLlmAdapter
from jb.core.ports.account_query_port import AccountQueryPort
from jb.core.ports.customer_directory_port import CustomerDirectoryPort
from jb.core.ports.llm_port import LlmPort


@lru_cache
def get_llm() -> LlmPort:
    """폴백 체인: Gemini → Groq → Mock. 키가 없으면 가드가 막고 다음 순위로 넘어간다."""
    return FallbackLlmAdapter(
        [
            GeminiAdapter(settings.gemini_api_key),
            GroqAdapter(settings.groq_api_key),
            MockLlmAdapter(),
        ]
    )


@lru_cache
def get_account_query() -> AccountQueryPort:
    return MockAccountQuery()


@lru_cache
def get_customer_directory() -> CustomerDirectoryPort:
    return MockCustomerDirectory()
