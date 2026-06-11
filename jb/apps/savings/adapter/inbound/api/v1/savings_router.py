from __future__ import annotations

from fastapi import APIRouter, Depends

from jb.apps.savings.adapter.inbound.api.schemas.savings_schema import (
    ProposeSavingsRequest,
    ProposeSavingsResponse,
)
from jb.apps.savings.app.dtos.savings_dto import ProposeSavingsCommand
from jb.apps.savings.app.ports.input.propose_savings_use_case import ProposeSavingsUseCase
from jb.apps.savings.dependencies.savings_provider import get_propose_savings_use_case

savings_router = APIRouter(prefix="/savings", tags=["savings"])


@savings_router.post("/propose", response_model=ProposeSavingsResponse)
async def propose_savings(
    body: ProposeSavingsRequest,
    usecase: ProposeSavingsUseCase = Depends(get_propose_savings_use_case),
) -> ProposeSavingsResponse:
    view = await usecase.execute(ProposeSavingsCommand(user_id=body.user_id))
    return ProposeSavingsResponse(
        idle_amount=view.idle_amount,
        monthly_interest=view.monthly_interest,
        rate=view.rate,
        ai_message=view.ai_message,
        agree_label=view.agree_label,
        reject_label=view.reject_label,
    )
