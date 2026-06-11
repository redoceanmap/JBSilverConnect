from __future__ import annotations

from jb.apps.reservation.app.dtos.reservation_dto import (
    ListReservationsQuery,
    ReservationView,
)
from jb.apps.reservation.app.ports.input.list_reservations_use_case import (
    ListReservationsUseCase,
)
from jb.apps.reservation.app.ports.output.reservation_repository_port import (
    ReservationRepositoryPort,
)
from jb.apps.reservation.app.use_cases.reservation_view_mapper import to_view
from jb.shared_kernel.value_objects import UserId


class ListReservationsInteractor(ListReservationsUseCase):
    """SRP: '사용자 예약 목록 조회'만 책임진다. DIP: 저장소 Port에만 의존."""

    def __init__(self, repository: ReservationRepositoryPort) -> None:
        self._repository = repository

    async def execute(self, query: ListReservationsQuery) -> list[ReservationView]:
        reservations = await self._repository.list_by_user(UserId(query.user_id))
        return [to_view(reservation) for reservation in reservations]
