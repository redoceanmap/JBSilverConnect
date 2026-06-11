from __future__ import annotations

from jb.apps.report.app.ports.output.report_repository import ReportRepositoryPort
from jb.apps.report.domain.value_objects.report_vo import MonthlyInterest
from jb.shared_kernel.value_objects import Money, UserId


class MockReportRepository(ReportRepositoryPort):
    """데모용 월별 이자 데이터. 실 서비스 전환 시 거래내역 어댑터로 교체 — 유스케이스 변경 0."""

    async def monthly_interests(self, user_id: UserId) -> list[MonthlyInterest]:
        return [
            MonthlyInterest("2026-01", Money(120)),
            MonthlyInterest("2026-02", Money(135)),
            MonthlyInterest("2026-03", Money(140)),
            MonthlyInterest("2026-04", Money(145)),
            MonthlyInterest("2026-05", Money(150)),
            MonthlyInterest("2026-06", Money(145)),
        ]
