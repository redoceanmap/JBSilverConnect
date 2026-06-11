from __future__ import annotations

from jb.apps.branch.app.dtos.branch_dto import BranchView, FindNearbyBranchesCommand
from jb.apps.branch.app.ports.input.find_nearby_branches_use_case import (
    FindNearbyBranchesUseCase,
)
from jb.apps.branch.app.ports.output.map_port import MapPort
from jb.apps.branch.domain.value_objects.branch_vo import GeoCoordinate


class FindNearbyBranchesInteractor(FindNearbyBranchesUseCase):
    """SRP: '주변 지점 조회 + 거리순 정렬'만 책임진다. DIP: MapPort에만 의존."""

    def __init__(self, map_provider: MapPort) -> None:
        self._map = map_provider

    async def execute(self, command: FindNearbyBranchesCommand) -> list[BranchView]:
        origin = GeoCoordinate(command.latitude, command.longitude)
        branches = await self._map.find_nearby(origin, command.limit)
        ordered = sorted(branches, key=lambda branch: branch.distance.meters)
        return [
            BranchView(
                name=branch.name,
                distance_meters=branch.distance.meters,
                waiting_count=branch.wait_status.waiting_count,
            )
            for branch in ordered
        ]
