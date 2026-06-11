from __future__ import annotations

from jb.apps.phishing.app.dtos.phishing_dto import CheckPhishingCommand, PhishingView
from jb.apps.phishing.app.ports.input.check_phishing_use_case import CheckPhishingUseCase
from jb.apps.phishing.app.use_cases.phishing_view_mapper import to_view
from jb.apps.phishing.domain.entities.phishing_assessment_entity import PhishingAssessment
from jb.apps.phishing.domain.services.risk_classification_policy import (
    RiskClassificationPolicy,
)
from jb.apps.phishing.app.ports.output.llm_port import PhishingLlmPort


class CheckPhishingInteractor(CheckPhishingUseCase):
    """
    SRP: '피싱 위험 판정'만 책임진다.
    DIP: LLM Port + 분류 정책(도메인 서비스)에만 의존. 분기는 정책의 다형 디스패치가 담당.
    """

    def __init__(self, llm: PhishingLlmPort, policy: RiskClassificationPolicy) -> None:
        self._llm = llm
        self._policy = policy

    async def execute(self, command: CheckPhishingCommand) -> PhishingView:
        verdict = await self._llm.generate(
            "다음 통화/문자가 보이스피싱인지 'safe', 'warning', 'danger' "
            f"중 한 단어로만 답해줘: {command.message}"
        )
        risk = self._policy.classify(verdict)
        assessment = PhishingAssessment(message=command.message, risk=risk)
        return to_view(assessment)
