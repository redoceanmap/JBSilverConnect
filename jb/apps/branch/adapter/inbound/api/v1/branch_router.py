from __future__ import annotations

from fastapi import APIRouter, Depends

from jb.apps.branch.adapter.inbound.api.schemas.branch_schema import (
    BranchItem,
    FindNearbyBranchesRequest,
)
from jb.apps.branch.app.dtos.branch_dto import FindNearbyBranchesCommand
from jb.apps.branch.app.ports.input.find_nearby_branches_use_case import (
    FindNearbyBranchesUseCase,
)
from jb.apps.branch.dependencies.branch_provider import get_find_nearby_branches_use_case

branch_router = APIRouter(prefix="/branch", tags=["branch"])


@branch_router.post("/nearby", response_model=list[BranchItem])
async def find_nearby_branches(
    body: FindNearbyBranchesRequest,
    usecase: FindNearbyBranchesUseCase = Depends(get_find_nearby_branches_use_case),
) -> list[BranchItem]:
    views = await usecase.execute(
        FindNearbyBranchesCommand(
            latitude=body.latitude,
            longitude=body.longitude,
            limit=body.limit,
        )
    )
    return [
        BranchItem(
            name=view.name,
            distance_meters=view.distance_meters,
            waiting_count=view.waiting_count,
            latitude=view.latitude,
            longitude=view.longitude,
        )
        for view in views
    ]
