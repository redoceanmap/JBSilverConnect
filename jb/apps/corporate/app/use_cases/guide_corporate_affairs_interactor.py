from __future__ import annotations

from jb.apps.corporate.app.dtos.corporate_dto import (
    CorporateGuideQuery,
    CorporateGuideView,
)
from jb.apps.corporate.app.ports.input.guide_corporate_affairs_use_case import (
    GuideCorporateAffairsUseCase,
)
from jb.apps.corporate.app.ports.output.corporate_guide_port import CorporateGuidePort
from jb.apps.corporate.app.use_cases.corporate_view_mapper import to_view
from jb.apps.corporate.domain.value_objects.corporate_vo import GeoPoint


class GuideCorporateAffairsInteractor(GuideCorporateAffairsUseCase):
    """SRP: '법인 사무 안내(서류·비용·최근접 기관) 조회'만 책임진다. DIP: CorporateGuidePort에만 의존."""

    def __init__(self, guide_provider: CorporateGuidePort) -> None:
        self._guide = guide_provider

    async def execute(self, query: CorporateGuideQuery) -> CorporateGuideView:
        origin = GeoPoint(query.latitude, query.longitude)
        guides = await self._guide.guide(origin, query.topic)
        return to_view(guides, query.topic)
