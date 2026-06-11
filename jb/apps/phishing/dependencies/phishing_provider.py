from __future__ import annotations

from jb.apps.phishing.adapter.outbound.core_llm_phishing_adapter import (
    CoreLlmPhishingAdapter,
)
from jb.apps.phishing.app.ports.input.check_phishing_use_case import CheckPhishingUseCase
from jb.apps.phishing.app.use_cases.check_phishing_interactor import CheckPhishingInteractor
from jb.apps.phishing.domain.services.risk_classification_policy import (
    RiskClassificationPolicy,
)
from jb.core.di import get_llm


def get_check_phishing_use_case() -> CheckPhishingUseCase:
    return CheckPhishingInteractor(
        llm=CoreLlmPhishingAdapter(get_llm()),
        policy=RiskClassificationPolicy(),
    )
