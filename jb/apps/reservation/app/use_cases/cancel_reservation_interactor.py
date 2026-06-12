from __future__ import annotations

from jb.apps.reservation.app.dtos.reservation_dto import (
    CancelReservationCommand,
    ReservationView,
)
from jb.apps.reservation.app.ports.input.cancel_reservation_use_case import (
    CancelReservationUseCase,
)
from jb.apps.reservation.app.ports.output.queue_registrar_port import QueueRegistrarPort
from jb.apps.reservation.app.ports.output.reservation_repository_port import (
    ReservationRepositoryPort,
)
from jb.apps.reservation.app.use_cases.reservation_view_mapper import to_view


class CancelReservationInteractor(CancelReservationUseCase):
    """SRP: '번호표 취소'만 책임진다. 취소 시 어드민 대기열에서도 제거한다. 기록은 이력으로 보존한다."""

    def __init__(
        self,
        repository: ReservationRepositoryPort,
        queue_registrar: QueueRegistrarPort,
    ) -> None:
        self._repository = repository
        self._queue_registrar = queue_registrar

    async def execute(self, command: CancelReservationCommand) -> ReservationView:
        reservation = await self._repository.get(command.reservation_id)
        if reservation is None:
            raise ValueError("예약을 찾을 수 없습니다")

        reservation.cancel()
        await self._repository.save(reservation)
        await self._queue_registrar.deregister(reservation.reservation_id)
        return to_view(reservation)
