from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.reservation.app.dtos.reservation_dto import (
    CancelReservationCommand,
    ReservationView,
)


class CancelReservationUseCase(ABC):
    """Driving Port — 번호표 취소 계약. 기록은 보존된다."""

    @abstractmethod
    async def execute(self, command: CancelReservationCommand) -> ReservationView: ...
