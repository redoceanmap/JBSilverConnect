from __future__ import annotations

from jb.apps.report.app.dtos.report_dto import InterestReportView, MonthlyInterestView
from jb.apps.report.domain.entities.interest_report_entity import InterestReport


def to_view(report: InterestReport) -> InterestReportView:
    return InterestReportView(
        total_interest=report.total_interest().amount,
        streak_months=report.streak().months,
        monthly=[
            MonthlyInterestView(month=record.month, amount=record.amount.amount)
            for record in report.records
        ],
    )
