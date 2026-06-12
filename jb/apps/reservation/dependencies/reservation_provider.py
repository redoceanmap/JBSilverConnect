from __future__ import annotations

from functools import lru_cache

from jb.apps.queue.dependencies.queue_provider import (
    get_register_queue_entry_use_case,
    get_remove_queue_entry_use_case,
)
from jb.apps.reservation.adapter.outbound.mock.in_memory_reservation_repository import (
    InMemoryReservationRepository,
)
from jb.apps.reservation.adapter.outbound.mock.mock_ticket_dispenser import (
    MockTicketDispenser,
)
from jb.apps.reservation.adapter.outbound.queue.reservation_queue_registrar_adapter import (
    ReservationQueueRegistrarAdapter,
)
from jb.apps.reservation.app.ports.input.cancel_reservation_use_case import (
    CancelReservationUseCase,
)
from jb.apps.reservation.app.ports.input.create_reservation_use_case import (
    CreateReservationUseCase,
)
from jb.apps.reservation.app.ports.input.list_queue_use_case import ListQueueUseCase
from jb.apps.reservation.app.ports.input.list_reservations_use_case import (
    ListReservationsUseCase,
)
from jb.apps.reservation.app.ports.output.reservation_repository_port import (
    ReservationRepositoryPort,
)
from jb.apps.reservation.app.ports.output.ticket_dispenser_port import TicketDispenserPort
from jb.apps.reservation.app.use_cases.cancel_reservation_interactor import (
    CancelReservationInteractor,
)
from jb.apps.reservation.app.use_cases.create_reservation_interactor import (
    CreateReservationInteractor,
)
from jb.apps.reservation.app.use_cases.list_queue_interactor import ListQueueInteractor
from jb.apps.reservation.app.use_cases.list_reservations_interactor import (
    ListReservationsInteractor,
)
from jb.core.customer.mock_customer_directory import MockCustomerDirectory
from jb.core.di import get_llm
from jb.core.ports.customer_directory_port import CustomerDirectoryPort


@lru_cache
def _get_ticket_dispenser() -> TicketDispenserPort:
    return MockTicketDispenser()


@lru_cache
def _get_reservation_repository() -> ReservationRepositoryPort:
    return InMemoryReservationRepository()


@lru_cache
def _get_customer_directory() -> CustomerDirectoryPort:
    return MockCustomerDirectory()


def _get_queue_registrar() -> ReservationQueueRegistrarAdapter:
    return ReservationQueueRegistrarAdapter(
        get_register_queue_entry_use_case(),
        get_remove_queue_entry_use_case(),
    )


def get_create_reservation_use_case() -> CreateReservationUseCase:
    return CreateReservationInteractor(
        dispenser=_get_ticket_dispenser(),
        repository=_get_reservation_repository(),
        customer_directory=_get_customer_directory(),
        queue_registrar=_get_queue_registrar(),
        llm=get_llm(),
    )


def get_list_reservations_use_case() -> ListReservationsUseCase:
    return ListReservationsInteractor(repository=_get_reservation_repository())


def get_list_queue_use_case() -> ListQueueUseCase:
    return ListQueueInteractor(repository=_get_reservation_repository())


def get_cancel_reservation_use_case() -> CancelReservationUseCase:
    return CancelReservationInteractor(
        repository=_get_reservation_repository(),
        queue_registrar=_get_queue_registrar(),
    )
