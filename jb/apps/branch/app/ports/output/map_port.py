from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.branch.domain.entities.branch_entity import Branch
from jb.apps.branch.domain.value_objects.branch_vo import GeoCoordinate


class MapPort(ABC):
    """지도/위치 추상화. 구현은 Adapter(Mock / 네이버 지역 검색 API)가 담당."""

    @abstractmethod
    async def find_nearby(self, origin: GeoCoordinate, limit: int) -> list[Branch]: ...
