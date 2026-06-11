from __future__ import annotations

from dataclasses import dataclass

from jb.apps.reservation.domain.value_objects.reservation_vo import TicketNumber
from jb.shared_kernel.domain_event import DomainEvent
from jb.shared_kernel.value_objects import UserId


@dataclass(frozen=True)
class ReservationCreated(DomainEvent):
    """번호표 발권이 완료되면 발생하는 과거형 도메인 이벤트."""

    user_id: UserId
    ticket: TicketNumber
