from __future__ import annotations

from pydantic import BaseModel, Field


class CreateReservationRequest(BaseModel):
    user_id: str = Field("user_kim_sonja", description="어르신 사용자 ID")
    purpose: str = Field("통장 정리", description="방문 목적")


class ReservationResponse(BaseModel):
    ticket_number: int
    purpose: str
    message: str
