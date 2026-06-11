from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    """금액 값 객체. 음수 불가, 원 단위. 불변."""

    amount: int

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("금액은 음수일 수 없습니다")

    def is_idle_over(self, threshold: "Money") -> bool:
        """유휴 잔액이 기준선 이상인지 — 분기 대신 도메인 의도를 드러내는 행위."""
        return self.amount >= threshold.amount


@dataclass(frozen=True)
class UserId:
    """사용자 식별자 값 객체. 빈 값 불가. 불변."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("UserId는 비어 있을 수 없습니다")
