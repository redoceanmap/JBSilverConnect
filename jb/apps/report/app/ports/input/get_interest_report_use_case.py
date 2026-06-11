from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.report.app.dtos.report_dto import GetInterestReportCommand, InterestReportView


class GetInterestReportUseCase(ABC):
    """Driving Port — 월별 이자 리포트 조회 유스케이스 계약."""

    @abstractmethod
    async def execute(self, command: GetInterestReportCommand) -> InterestReportView: ...
