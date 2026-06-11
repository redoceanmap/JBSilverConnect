from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.branch.app.dtos.branch_dto import BranchView, FindNearbyBranchesCommand


class FindNearbyBranchesUseCase(ABC):
    """Driving Port — 주변 지점 조회 유스케이스 계약."""

    @abstractmethod
    async def execute(self, command: FindNearbyBranchesCommand) -> list[BranchView]: ...
