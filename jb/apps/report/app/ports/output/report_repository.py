from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.report.domain.value_objects.report_vo import MonthlyInterest
from jb.shared_kernel.value_objects import UserId


class ReportRepositoryPort(ABC):
    """월별 이자 데이터 조회 추상화. 구현은 Adapter(Mock / 실 거래내역)가 담당."""

    @abstractmethod
    async def monthly_interests(self, user_id: UserId) -> list[MonthlyInterest]: ...
