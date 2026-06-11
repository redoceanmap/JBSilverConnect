from __future__ import annotations

from fastapi import APIRouter, Depends

from jb.apps.report.adapter.inbound.api.schemas.report_schema import (
    GetInterestReportRequest,
    InterestReportResponse,
    MonthlyInterestItem,
)
from jb.apps.report.app.dtos.report_dto import GetInterestReportCommand
from jb.apps.report.app.ports.input.get_interest_report_use_case import (
    GetInterestReportUseCase,
)
from jb.apps.report.dependencies.report_provider import get_interest_report_use_case

report_router = APIRouter(prefix="/report", tags=["report"])


@report_router.post("/interest", response_model=InterestReportResponse)
async def get_interest_report(
    body: GetInterestReportRequest,
    usecase: GetInterestReportUseCase = Depends(get_interest_report_use_case),
) -> InterestReportResponse:
    view = await usecase.execute(GetInterestReportCommand(user_id=body.user_id))
    return InterestReportResponse(
        total_interest=view.total_interest,
        streak_months=view.streak_months,
        monthly=[
            MonthlyInterestItem(month=item.month, amount=item.amount)
            for item in view.monthly
        ],
    )
