from __future__ import annotations

from fastapi import APIRouter, Depends

from jb.apps.corporate.adapter.inbound.api.schemas.corporate_schema import (
    CorporateGuidanceRequest,
    CorporateGuidanceResponse,
    CorporateTaskItem,
    InstitutionItem,
)
from jb.apps.corporate.app.dtos.corporate_dto import (
    CorporateGuideQuery,
    CorporateGuideView,
)
from jb.apps.corporate.app.ports.input.guide_corporate_affairs_use_case import (
    GuideCorporateAffairsUseCase,
)
from jb.apps.corporate.dependencies.corporate_provider import (
    get_guide_corporate_affairs_use_case,
)

corporate_router = APIRouter(prefix="/corporate", tags=["corporate"])


def _to_response(view: CorporateGuideView) -> CorporateGuidanceResponse:
    return CorporateGuidanceResponse(
        message=view.message,
        tasks=[
            CorporateTaskItem(
                task_name=task.task_name,
                required_docs=list(task.required_docs),
                estimated_cost=task.estimated_cost,
                institutions=[
                    InstitutionItem(
                        name=institution.name,
                        kind=institution.kind,
                        distance_meters=institution.distance_meters,
                    )
                    for institution in task.institutions
                ],
            )
            for task in view.tasks
        ],
    )


@corporate_router.post("/guidance", response_model=CorporateGuidanceResponse)
async def guide_corporate_affairs(
    body: CorporateGuidanceRequest,
    usecase: GuideCorporateAffairsUseCase = Depends(get_guide_corporate_affairs_use_case),
) -> CorporateGuidanceResponse:
    """창업·법인 사무 안내 — 업무별 필요 서류·예상 비용·사용자 위치 기준 최근접 기관."""
    view = await usecase.execute(
        CorporateGuideQuery(
            user_id=body.user_id,
            latitude=body.latitude,
            longitude=body.longitude,
            topic=body.topic,
        )
    )
    return _to_response(view)
