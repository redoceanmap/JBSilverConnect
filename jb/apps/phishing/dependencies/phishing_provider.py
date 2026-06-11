from __future__ import annotations

from jb.apps.phishing.adapter.outbound.core_llm_phishing_adapter import (
    CoreLlmPhishingAdapter,
)
from jb.apps.phishing.adapter.outbound.fallback_phishing_llm_adapter import (
    FallbackPhishingLlmAdapter,
)
from jb.apps.phishing.adapter.outbound.mock.mock_llm_adapter import MockPhishingLlmAdapter
from jb.apps.phishing.app.ports.input.check_phishing_use_case import CheckPhishingUseCase
from jb.apps.phishing.app.use_cases.check_phishing_interactor import CheckPhishingInteractor
from jb.apps.phishing.domain.services.risk_classification_policy import (
    RiskClassificationPolicy,
)
from jb.core.config import settings
from jb.core.llm.gemini_adapter import GeminiAdapter
from jb.core.llm.groq_adapter import GroqAdapter


def get_check_phishing_use_case() -> CheckPhishingUseCase:
    """폴백 체인: Gemini → Groq → Mock(룰베이스). 키가 없으면 가드가 막고 다음 순위로 넘어간다."""
    llm = FallbackPhishingLlmAdapter(
        [
            CoreLlmPhishingAdapter(GeminiAdapter(settings.gemini_api_key)),
            CoreLlmPhishingAdapter(GroqAdapter(settings.groq_api_key)),
            MockPhishingLlmAdapter(),
        ]
    )
    return CheckPhishingInteractor(
        llm=llm,
        policy=RiskClassificationPolicy(),
    )
