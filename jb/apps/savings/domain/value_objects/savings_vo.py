from __future__ import annotations

from dataclasses import dataclass

from jb.shared_kernel.value_objects import Money


@dataclass(frozen=True)
class InterestRate:
    """연이율 값 객체. 불변. 음수 불가. 이자 계산 행위를 직접 보유(tell-don't-ask)."""

    annual: float

    def __post_init__(self) -> None:
        if self.annual < 0:
            raise ValueError("연이율은 음수일 수 없습니다")

    def monthly_interest_of(self, principal: Money) -> Money:
        return Money(int(principal.amount * self.annual / 12))

    def as_percent(self) -> float:
        return round(self.annual * 100, 2)
