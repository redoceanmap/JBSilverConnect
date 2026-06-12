from __future__ import annotations

from pydantic import BaseModel, Field


class FindNearbyBranchesRequest(BaseModel):
    latitude: float = Field(37.5665, description="현재 위도")
    longitude: float = Field(126.9780, description="현재 경도")
    limit: int = Field(3, description="조회할 지점 수")


class BranchItem(BaseModel):
    name: str
    distance_meters: int
    waiting_count: int
    latitude: float
    longitude: float
