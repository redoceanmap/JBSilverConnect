from __future__ import annotations

from jb.apps.reservation.app.dtos.reservation_dto import ReservationView
from jb.apps.reservation.app.ports.input.list_queue_use_case import ListQueueUseCase
from jb.apps.reservation.app.ports.output.reservation_repository_port import (
    ReservationRepositoryPort,
)
from jb.apps.reservation.app.use_cases.reservation_view_mapper import to_view


class ListQueueInteractor(ListQueueUseCase):
    """SRP: '창구 대기열(전체 활성 번호표) 조회 + 번호순 정렬'만 책임진다. DIP: 저장소 Port에만 의존."""

    def __init__(self, repository: ReservationRepositoryPort) -> None:
        self._repository = repository

    async def execute(self) -> list[ReservationView]:
        reservations = await self._repository.list_active_all()
        ordered = sorted(reservations, key=lambda reservation: reservation.ticket.value)
        return [to_view(reservation) for reservation in ordered]
