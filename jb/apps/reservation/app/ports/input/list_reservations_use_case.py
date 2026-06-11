from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.reservation.app.dtos.reservation_dto import (
    ListReservationsQuery,
    ReservationView,
)


class ListReservationsUseCase(ABC):
    """Driving Port — 사용자의 예약 번호표 목록 조회 계약."""

    @abstractmethod
    async def execute(self, query: ListReservationsQuery) -> list[ReservationView]: ...
