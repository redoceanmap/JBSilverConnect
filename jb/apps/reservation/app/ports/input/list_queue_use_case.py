from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.reservation.app.dtos.reservation_dto import ReservationView


class ListQueueUseCase(ABC):
    """Driving Port — 창구(어드민)용 전체 활성 번호표 대기열 조회 계약."""

    @abstractmethod
    async def execute(self) -> list[ReservationView]: ...
