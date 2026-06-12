from __future__ import annotations

from pydantic import BaseModel, Field


class CorporateGuidanceRequest(BaseModel):
    user_id: str = Field("user_kim_sonja", description="고객님 사용자 ID")
    latitude: float = Field(37.5665, description="현재 위도")
    longitude: float = Field(126.9780, description="현재 경도")
    topic: str = Field("corporate", description="안내 주제: 'corporate'(법인 사무) 또는 'mortgage'(부동산 담보대출)")


class InstitutionItem(BaseModel):
    name: str
    kind: str
    distance_meters: int


class CorporateTaskItem(BaseModel):
    task_name: str
    required_docs: list[str]
    estimated_cost: str
    institutions: list[InstitutionItem]


class CorporateGuidanceResponse(BaseModel):
    message: str
    tasks: list[CorporateTaskItem]
