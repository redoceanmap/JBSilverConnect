from __future__ import annotations

from dataclasses import dataclass, field

from jb.apps.reservation.domain.events.reservation_events import ReservationCreated
from jb.apps.reservation.domain.value_objects.reservation_vo import (
    Purpose,
    ReservationStatus,
    TicketNumber,
)
from jb.shared_kernel.domain_event import DomainEvent
from jb.shared_kernel.value_objects import UserId, WindowType


@dataclass
class Reservation:
    """지점 방문 예약 — Aggregate Root. 생성 시 번호표 발권 이벤트가 발생한다."""

    reservation_id: str
    user_id: UserId
    purpose: Purpose
    ticket: TicketNumber
    branch_name: str | None = None
    note: str | None = None
    window_type: WindowType = WindowType.GENERAL
    status: ReservationStatus = ReservationStatus.ACTIVE
    _events: list[DomainEvent] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self._events.append(ReservationCreated(user_id=self.user_id, ticket=self.ticket))

    def ticket_label(self) -> str:
        """창구 종류 접두가 붙은 번호표 표기. 예: 법인 3번 → 'B3'."""
        return self.window_type.format_ticket(self.ticket.value)

    def guidance(self) -> str:
        base = f"{self.ticket_label()}번 번호표가 발급되었습니다. 창구에서 '{self.purpose.value}'를 도와드릴게요."
        if self.branch_name:
            base = f"[{self.branch_name}] " + base
        return base

    def cancel(self) -> None:
        """번호표를 취소한다. 기록(지점·목적·메모)은 이력으로 보존된다."""
        self.status = ReservationStatus.CANCELED

    def pull_events(self) -> list[DomainEvent]:
        events = self._events
        self._events = []
        return events
