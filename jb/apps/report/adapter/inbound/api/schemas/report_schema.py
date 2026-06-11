from __future__ import annotations

from pydantic import BaseModel, Field


class GetInterestReportRequest(BaseModel):
    user_id: str = Field("user_kim_sonja", description="어르신 사용자 ID")


class MonthlyInterestItem(BaseModel):
    month: str
    amount: int


class InterestReportResponse(BaseModel):
    total_interest: int
    streak_months: int
    monthly: list[MonthlyInterestItem]
