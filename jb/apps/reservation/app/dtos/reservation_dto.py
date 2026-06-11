from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateReservationCommand:
    user_id: str
    purpose: str


@dataclass(frozen=True)
class ReservationView:
    ticket_number: int
    purpose: str
    message: str
