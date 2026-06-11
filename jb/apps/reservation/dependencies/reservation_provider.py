from __future__ import annotations

from functools import lru_cache

from jb.apps.reservation.adapter.outbound.mock.mock_ticket_dispenser import (
    MockTicketDispenser,
)
from jb.apps.reservation.app.ports.input.create_reservation_use_case import (
    CreateReservationUseCase,
)
from jb.apps.reservation.app.ports.output.ticket_dispenser_port import TicketDispenserPort
from jb.apps.reservation.app.use_cases.create_reservation_interactor import (
    CreateReservationInteractor,
)


@lru_cache
def _get_ticket_dispenser() -> TicketDispenserPort:
    return MockTicketDispenser()


def get_create_reservation_use_case() -> CreateReservationUseCase:
    return CreateReservationInteractor(dispenser=_get_ticket_dispenser())
