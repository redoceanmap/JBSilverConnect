from __future__ import annotations

from jb.apps.report.app.dtos.report_dto import (
    GetInterestReportCommand,
    InterestReportView,
)
from jb.apps.report.app.ports.input.get_interest_report_use_case import (
    GetInterestReportUseCase,
)
from jb.apps.report.app.ports.output.report_repository import ReportRepositoryPort
from jb.apps.report.app.use_cases.report_view_mapper import to_view
from jb.apps.report.domain.entities.interest_report_entity import InterestReport
from jb.shared_kernel.value_objects import UserId


class GetInterestReportInteractor(GetInterestReportUseCase):
    """SRP: '이자 리포트 조회 + 집계'만 책임진다. DIP: 리포지토리 Port에만 의존."""

    def __init__(self, repository: ReportRepositoryPort) -> None:
        self._repository = repository

    async def execute(self, command: GetInterestReportCommand) -> InterestReportView:
        records = await self._repository.monthly_interests(UserId(command.user_id))
        report = InterestReport(records=records)
        return to_view(report)
