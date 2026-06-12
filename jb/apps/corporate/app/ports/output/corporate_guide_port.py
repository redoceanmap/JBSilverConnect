from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.corporate.domain.value_objects.corporate_vo import (
    CorporateTaskGuide,
    GeoPoint,
)


class CorporateGuidePort(ABC):
    """방문 준비(필요 서류) 안내 추상화. 구현은 Adapter(큐레이션 Mock 등)가 담당."""

    @abstractmethod
    async def guide(self, origin: GeoPoint, topic: str) -> list[CorporateTaskGuide]:
        """주제(법인 사무·부동산 담보대출 등)별로 필요 서류·비용·최근접 발급 기관을 돌려준다."""
        ...
