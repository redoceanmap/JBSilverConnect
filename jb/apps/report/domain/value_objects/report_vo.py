from __future__ import annotations

from dataclasses import dataclass

from jb.shared_kernel.value_objects import Money


@dataclass(frozen=True)
class MonthlyInterest:
    """월별 이자 값 객체. 불변."""

    month: str
    amount: Money

    def __post_init__(self) -> None:
        if not self.month:
            raise ValueError("월 정보는 비어 있을 수 없습니다")


@dataclass(frozen=True)
class InterestStreak:
    """연속으로 이자가 발생한 개월 수 값 객체. 음수 불가. 불변."""

    months: int

    def __post_init__(self) -> None:
        if self.months < 0:
            raise ValueError("연속 개월 수는 음수일 수 없습니다")
