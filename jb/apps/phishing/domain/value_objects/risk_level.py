from __future__ import annotations

from abc import ABC, abstractmethod


class RiskLevel(ABC):
    """
    위험도 값 객체 — 다형 패밀리.
    safe/warning/danger를 if-else로 분기하지 않고, 각 위험도가 자신의 행동을 직접 안다(OCP).
    새 위험도 추가 시 기존 코드를 수정하지 않고 구현체만 추가한다.
    """

    @abstractmethod
    def label(self) -> str: ...

    @abstractmethod
    def signal_color(self) -> str: ...

    @abstractmethod
    def should_alert_staff(self) -> bool: ...

    @abstractmethod
    def advice(self) -> str: ...


class SafeRisk(RiskLevel):
    def label(self) -> str:
        return "safe"

    def signal_color(self) -> str:
        return "green"

    def should_alert_staff(self) -> bool:
        return False

    def advice(self) -> str:
        return "안심하셔도 됩니다. 평소처럼 진행하세요."


class WarningRisk(RiskLevel):
    def label(self) -> str:
        return "warning"

    def signal_color(self) -> str:
        return "yellow"

    def should_alert_staff(self) -> bool:
        return True

    def advice(self) -> str:
        return "잠시 멈추세요. 가족이나 창구 직원에게 먼저 확인하는 것이 좋겠습니다."


class DangerRisk(RiskLevel):
    def label(self) -> str:
        return "danger"

    def signal_color(self) -> str:
        return "red"

    def should_alert_staff(self) -> bool:
        return True

    def advice(self) -> str:
        return "절대 송금하지 마세요. 즉시 창구 직원에게 알렸습니다."
