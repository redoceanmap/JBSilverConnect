from __future__ import annotations

from fastapi import APIRouter, Depends

from jb.apps.phishing.adapter.inbound.api.schemas.phishing_schema import (
    CheckPhishingRequest,
    PhishingResponse,
)
from jb.apps.phishing.app.dtos.phishing_dto import CheckPhishingCommand
from jb.apps.phishing.app.ports.input.check_phishing_use_case import CheckPhishingUseCase
from jb.apps.phishing.dependencies.phishing_provider import get_check_phishing_use_case

phishing_router = APIRouter(prefix="/phishing", tags=["phishing"])


@phishing_router.post("/check", response_model=PhishingResponse)
async def check_phishing(
    body: CheckPhishingRequest,
    usecase: CheckPhishingUseCase = Depends(get_check_phishing_use_case),
) -> PhishingResponse:
    view = await usecase.execute(CheckPhishingCommand(message=body.message))
    return PhishingResponse(
        risk_label=view.risk_label,
        signal_color=view.signal_color,
        alert_staff=view.alert_staff,
        advice=view.advice,
    )
