from __future__ import annotations

from uuid import uuid4

from jb.apps.reservation.app.dtos.reservation_dto import (
    CreateReservationCommand,
    ReservationView,
)
from jb.apps.reservation.app.ports.input.create_reservation_use_case import (
    CreateReservationUseCase,
)
from jb.apps.reservation.app.ports.output.reservation_repository_port import (
    ReservationRepositoryPort,
)
from jb.apps.reservation.app.ports.output.ticket_dispenser_port import TicketDispenserPort
from jb.apps.reservation.app.use_cases.reservation_view_mapper import to_view
from jb.apps.reservation.domain.entities.reservation_entity import Reservation
from jb.apps.reservation.domain.value_objects.reservation_vo import Purpose
from jb.shared_kernel.value_objects import UserId


class CreateReservationInteractor(CreateReservationUseCase):
    """SRP: '예약 생성 + 번호표 발권'만 책임진다. DIP: 발급기·저장소 Port에만 의존."""

    def __init__(
        self,
        dispenser: TicketDispenserPort,
        repository: ReservationRepositoryPort,
    ) -> None:
        self._dispenser = dispenser
        self._repository = repository

    async def execute(self, command: CreateReservationCommand) -> ReservationView:
        user_id = UserId(command.user_id)

        # 같은 지점에 이미 활성 번호표가 있으면 중복 발권하지 않고 그대로 돌려준다.
        existing = await self._repository.find_active(user_id, command.branch_name)
        if existing is not None:
            return to_view(existing)

        ticket = await self._dispenser.next_ticket()
        reservation = Reservation(
            reservation_id=uuid4().hex,
            user_id=user_id,
            purpose=Purpose(command.purpose),
            ticket=ticket,
            branch_name=command.branch_name,
            note=command.note,
        )
        await self._repository.save(reservation)
        return to_view(reservation)
