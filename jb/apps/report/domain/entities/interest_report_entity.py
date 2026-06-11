from __future__ import annotations

from dataclasses import dataclass
from itertools import takewhile

from jb.apps.report.domain.value_objects.report_vo import InterestStreak, MonthlyInterest
from jb.shared_kernel.value_objects import Money


@dataclass
class InterestReport:
    """월별 이자 리포트 — Aggregate Root."""

    records: list[MonthlyInterest]

    def total_interest(self) -> Money:
        return Money(sum(record.amount.amount for record in self.records))

    def streak(self) -> InterestStreak:
        # 최근 월부터 거꾸로, 이자가 0보다 큰 동안만 센다 (분기 대신 takewhile).
        recent_positives = takewhile(
            lambda record: record.amount.amount > 0, reversed(self.records)
        )
        return InterestStreak(len(list(recent_positives)))
