from __future__ import annotations

from dataclasses import dataclass

from jb.apps.phishing.domain.value_objects.risk_level import RiskLevel


@dataclass
class PhishingAssessment:
    """
    피싱 위험 평가 — Aggregate Root.
    위험도 판단은 RiskLevel 다형 객체에 위임한다(tell-don't-ask, 분기 없음).
    """

    message: str
    risk: RiskLevel

    def __post_init__(self) -> None:
        if not self.message:
            raise ValueError("평가할 메시지는 비어 있을 수 없습니다")

    def risk_label(self) -> str:
        return self.risk.label()

    def signal_color(self) -> str:
        return self.risk.signal_color()

    def should_alert_staff(self) -> bool:
        return self.risk.should_alert_staff()

    def advice(self) -> str:
        return self.risk.advice()
