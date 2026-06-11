from __future__ import annotations

from pydantic import BaseModel, Field


class GenerateBriefingRequest(BaseModel):
    user_id: str = Field("user_kim_sonja", description="어르신 사용자 ID")


class BriefingResponse(BaseModel):
    balance: int
    weather_description: str
    temperature: int
    spoken_text: str
    audio_size_bytes: int
