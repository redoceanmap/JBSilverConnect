from __future__ import annotations

from jb.apps.branch.adapter.outbound.fallback_map_adapter import FallbackMapAdapter
from jb.apps.branch.adapter.outbound.mock.mock_map_adapter import MockMapAdapter
from jb.apps.branch.adapter.outbound.naver.naver_map_adapter import NaverMapAdapter
from jb.apps.branch.app.ports.input.find_nearby_branches_use_case import (
    FindNearbyBranchesUseCase,
)
from jb.apps.branch.app.use_cases.find_nearby_branches_interactor import (
    FindNearbyBranchesInteractor,
)
from jb.core.config import settings


def get_find_nearby_branches_use_case() -> FindNearbyBranchesUseCase:
    """폴백 체인: Naver → Mock. 키가 없거나 호출 실패 시 Mock 데모 데이터로 폴백한다."""
    map_provider = FallbackMapAdapter(
        [
            NaverMapAdapter(settings.naver_client_id, settings.naver_client_secret),
            MockMapAdapter(),
        ]
    )
    return FindNearbyBranchesInteractor(map_provider=map_provider)
