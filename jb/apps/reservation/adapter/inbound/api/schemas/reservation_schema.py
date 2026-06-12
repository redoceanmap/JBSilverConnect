from __future__ import annotations

from pydantic import BaseModel, Field


class CreateReservationRequest(BaseModel):
    user_id: str = Field("user_kim_sonja", description="고객님 사용자 ID")
    purpose: str = Field("통장 정리", description="방문 목적")
    branch_name: str | None = Field(None, description="방문 지점명")
    note: str | None = Field(None, description="창구 전달 메모")
    window_type: str = Field("general", description="창구 종류: 'general' 또는 'corporate'(법인 사무)")


class ReservationResponse(BaseModel):
    reservation_id: str
    ticket_number: int
    ticket_label: str
    window_type: str
    purpose: str
    message: str
    status: str
    branch_name: str | None = None
    note: str | None = None
