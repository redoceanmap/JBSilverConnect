from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.reservation.app.dtos.reservation_dto import (
    CreateReservationCommand,
    ReservationView,
)


class CreateReservationUseCase(ABC):
    """Driving Port — 번호표 발권 유스케이스 계약."""

    @abstractmethod
    async def execute(self, command: CreateReservationCommand) -> ReservationView: ...
