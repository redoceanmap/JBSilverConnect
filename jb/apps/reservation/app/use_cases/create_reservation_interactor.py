from __future__ import annotations

from jb.apps.reservation.app.dtos.reservation_dto import (
    CreateReservationCommand,
    ReservationView,
)
from jb.apps.reservation.app.ports.input.create_reservation_use_case import (
    CreateReservationUseCase,
)
from jb.apps.reservation.app.ports.output.ticket_dispenser_port import TicketDispenserPort
from jb.apps.reservation.domain.entities.reservation_entity import Reservation
from jb.apps.reservation.domain.value_objects.reservation_vo import Purpose
from jb.shared_kernel.value_objects import UserId


class CreateReservationInteractor(CreateReservationUseCase):
    """SRP: '예약 생성 + 번호표 발권'만 책임진다. DIP: 발급기 Port에만 의존."""

    def __init__(self, dispenser: TicketDispenserPort) -> None:
        self._dispenser = dispenser

    async def execute(self, command: CreateReservationCommand) -> ReservationView:
        ticket = await self._dispenser.next_ticket()
        reservation = Reservation(
            user_id=UserId(command.user_id),
            purpose=Purpose(command.purpose),
            ticket=ticket,
        )
        return ReservationView(
            ticket_number=ticket.value,
            purpose=command.purpose,
            message=reservation.guidance(),
        )
