from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateReservationCommand:
    user_id: str
    purpose: str
    branch_name: str | None = None
    note: str | None = None


@dataclass(frozen=True)
class ListReservationsQuery:
    user_id: str


@dataclass(frozen=True)
class CancelReservationCommand:
    reservation_id: str


@dataclass(frozen=True)
class ReservationView:
    reservation_id: str
    ticket_number: int
    purpose: str
    message: str
    status: str
    branch_name: str | None = None
    note: str | None = None
