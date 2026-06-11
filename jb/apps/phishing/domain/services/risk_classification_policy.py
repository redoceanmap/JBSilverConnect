from __future__ import annotations

from jb.apps.phishing.domain.value_objects.risk_level import (
    DangerRisk,
    RiskLevel,
    SafeRisk,
    WarningRisk,
)


class RiskClassificationPolicy:
    """
    라벨 → RiskLevel 매핑 도메인 서비스.
    if-else/switch 대신 dict 디스패치로 다형 구현체를 선택한다.
    알 수 없는 라벨은 보수적으로 경고(WarningRisk)로 처리한다.
    """

    def __init__(self) -> None:
        self._registry: dict[str, RiskLevel] = {
            "safe": SafeRisk(),
            "warning": WarningRisk(),
            "danger": DangerRisk(),
        }

    def classify(self, label: str) -> RiskLevel:
        return self._registry.get(label.strip().lower(), WarningRisk())
