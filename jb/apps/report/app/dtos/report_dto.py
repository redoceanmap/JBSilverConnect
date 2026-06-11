from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GetInterestReportCommand:
    user_id: str


@dataclass(frozen=True)
class MonthlyInterestView:
    month: str
    amount: int


@dataclass(frozen=True)
class InterestReportView:
    total_interest: int
    streak_months: int
    monthly: list[MonthlyInterestView]
