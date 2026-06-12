from __future__ import annotations

from jb.apps.branch.app.dtos.branch_dto import BranchView
from jb.apps.branch.domain.entities.branch_entity import Branch


def to_view(branch: Branch) -> BranchView:
    return BranchView(
        name=branch.name,
        distance_meters=branch.distance.meters,
        waiting_count=branch.wait_status.waiting_count,
        latitude=branch.coordinate.latitude,
        longitude=branch.coordinate.longitude,
    )
