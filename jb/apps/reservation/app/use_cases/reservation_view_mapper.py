from __future__ import annotations

from jb.apps.reservation.app.dtos.reservation_dto import ReservationView
from jb.apps.reservation.domain.entities.reservation_entity import Reservation


def to_view(reservation: Reservation) -> ReservationView:
    return ReservationView(
        reservation_id=reservation.reservation_id,
        ticket_number=reservation.ticket.value,
        ticket_label=reservation.ticket_label(),
        window_type=reservation.window_type.code,
        purpose=reservation.purpose.value,
        message=reservation.guidance(),
        status=reservation.status.value,
        branch_name=reservation.branch_name,
        note=reservation.note,
    )
