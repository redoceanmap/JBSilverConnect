from __future__ import annotations

from functools import lru_cache

from jb.apps.corporate.adapter.outbound.mock.mock_corporate_guide_adapter import (
    MockCorporateGuideAdapter,
)
from jb.apps.corporate.app.ports.input.guide_corporate_affairs_use_case import (
    GuideCorporateAffairsUseCase,
)
from jb.apps.corporate.app.ports.output.corporate_guide_port import CorporateGuidePort
from jb.apps.corporate.app.use_cases.guide_corporate_affairs_interactor import (
    GuideCorporateAffairsInteractor,
)


@lru_cache
def _get_corporate_guide_provider() -> CorporateGuidePort:
    return MockCorporateGuideAdapter()


def get_guide_corporate_affairs_use_case() -> GuideCorporateAffairsUseCase:
    return GuideCorporateAffairsInteractor(guide_provider=_get_corporate_guide_provider())
