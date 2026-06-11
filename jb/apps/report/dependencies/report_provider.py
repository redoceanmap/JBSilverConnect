from __future__ import annotations

from jb.apps.report.adapter.outbound.mock.mock_report_repository import MockReportRepository
from jb.apps.report.app.ports.input.get_interest_report_use_case import (
    GetInterestReportUseCase,
)
from jb.apps.report.app.use_cases.get_interest_report_interactor import (
    GetInterestReportInteractor,
)


def get_interest_report_use_case() -> GetInterestReportUseCase:
    return GetInterestReportInteractor(repository=MockReportRepository())
