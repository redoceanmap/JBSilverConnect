from __future__ import annotations

from dataclasses import dataclass, field

from jb.apps.reservation.domain.events.reservation_events import ReservationCreated
from jb.apps.reservation.domain.value_objects.reservation_vo import Purpose, TicketNumber
from jb.shared_kernel.domain_event import DomainEvent
from jb.shared_kernel.value_objects import UserId


@dataclass
class Reservation:
    """지점 방문 예약 — Aggregate Root. 생성 시 번호표 발권 이벤트가 발생한다."""

    user_id: UserId
    purpose: Purpose
    ticket: TicketNumber
    _events: list[DomainEvent] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self._events.append(ReservationCreated(user_id=self.user_id, ticket=self.ticket))

    def guidance(self) -> str:
        return f"{self.ticket.value}번 번호표가 발급되었습니다. 창구에서 '{self.purpose.value}'를 도와드릴게요."

    def pull_events(self) -> list[DomainEvent]:
        events = self._events
        self._events = []
        return events
