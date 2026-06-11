from __future__ import annotations

from jb.apps.branch.adapter.outbound.mock.mock_map_adapter import MockMapAdapter
from jb.apps.branch.app.ports.input.find_nearby_branches_use_case import (
    FindNearbyBranchesUseCase,
)
from jb.apps.branch.app.use_cases.find_nearby_branches_interactor import (
    FindNearbyBranchesInteractor,
)


def get_find_nearby_branches_use_case() -> FindNearbyBranchesUseCase:
    return FindNearbyBranchesInteractor(map_provider=MockMapAdapter())
