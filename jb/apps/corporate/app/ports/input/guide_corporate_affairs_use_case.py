from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.corporate.app.dtos.corporate_dto import (
    CorporateGuideQuery,
    CorporateGuideView,
)


class GuideCorporateAffairsUseCase(ABC):
    """Driving Port — 법인 사무 안내 유스케이스 계약."""

    @abstractmethod
    async def execute(self, query: CorporateGuideQuery) -> CorporateGuideView: ...
