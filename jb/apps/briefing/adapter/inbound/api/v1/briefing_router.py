from __future__ import annotations

from fastapi import APIRouter, Depends

from jb.apps.briefing.adapter.inbound.api.schemas.briefing_schema import (
    BriefingResponse,
    GenerateBriefingRequest,
)
from jb.apps.briefing.app.dtos.briefing_dto import GenerateBriefingCommand
from jb.apps.briefing.app.ports.input.generate_briefing_use_case import (
    GenerateBriefingUseCase,
)
from jb.apps.briefing.dependencies.briefing_provider import get_generate_briefing_use_case

briefing_router = APIRouter(prefix="/briefing", tags=["briefing"])


@briefing_router.post("/daily", response_model=BriefingResponse)
async def generate_briefing(
    body: GenerateBriefingRequest,
    usecase: GenerateBriefingUseCase = Depends(get_generate_briefing_use_case),
) -> BriefingResponse:
    view = await usecase.execute(GenerateBriefingCommand(user_id=body.user_id))
    return BriefingResponse(
        balance=view.balance,
        weather_description=view.weather_description,
        temperature=view.temperature,
        spoken_text=view.spoken_text,
        audio_size_bytes=view.audio_size_bytes,
    )
