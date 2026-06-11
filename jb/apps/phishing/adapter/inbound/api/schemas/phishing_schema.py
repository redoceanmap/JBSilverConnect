from __future__ import annotations

from pydantic import BaseModel, Field


class CheckPhishingRequest(BaseModel):
    message: str = Field(
        "검찰청인데요, 당신 계좌가 범죄에 연루되어 지금 송금하셔야 합니다",
        description="의심스러운 통화/문자 내용",
    )


class PhishingResponse(BaseModel):
    risk_label: str
    signal_color: str
    alert_staff: bool
    advice: str
