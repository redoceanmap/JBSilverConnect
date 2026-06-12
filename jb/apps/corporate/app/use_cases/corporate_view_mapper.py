from __future__ import annotations

from jb.apps.corporate.app.dtos.corporate_dto import (
    CorporateGuideView,
    CorporateTaskView,
    InstitutionView,
)
from jb.apps.corporate.domain.value_objects.corporate_vo import CorporateTaskGuide

_MESSAGES = {
    "corporate": (
        "창업·법인 사무는 아래 준비가 필요해요. "
        "업무마다 필요한 서류와 예상 비용, 그리고 가까운 발급 기관을 함께 안내해 드릴게요."
    ),
    "mortgage": (
        "부동산 담보대출에는 아래 서류가 필요해요. "
        "서류마다 발급처와 예상 비용, 가까운 발급 기관을 함께 안내해 드릴게요."
    ),
}


def to_view(guides: list[CorporateTaskGuide], topic: str) -> CorporateGuideView:
    return CorporateGuideView(
        message=_MESSAGES.get(topic, _MESSAGES["corporate"]),
        tasks=tuple(_to_task_view(guide) for guide in guides),
    )


def _to_task_view(guide: CorporateTaskGuide) -> CorporateTaskView:
    return CorporateTaskView(
        task_name=guide.task_name,
        required_docs=guide.required_docs,
        estimated_cost=guide.estimated_cost,
        institutions=tuple(
            InstitutionView(
                name=institution.name,
                kind=institution.kind,
                distance_meters=institution.distance_meters,
            )
            for institution in guide.institutions
        ),
    )
