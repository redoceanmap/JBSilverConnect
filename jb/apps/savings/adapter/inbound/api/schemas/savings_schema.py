from __future__ import annotations

from pydantic import BaseModel, Field


class ProposeSavingsRequest(BaseModel):
    user_id: str = Field("user_kim_sonja", description="어르신 사용자 ID")


class ProposeSavingsResponse(BaseModel):
    idle_amount: int
    monthly_interest: int
    rate: float
    ai_message: str
    agree_label: str
    reject_label: str
