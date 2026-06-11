from __future__ import annotations

from itertools import count

from jb.apps.reservation.app.ports.output.ticket_dispenser_port import TicketDispenserPort
from jb.apps.reservation.domain.value_objects.reservation_vo import TicketNumber


class MockTicketDispenser(TicketDispenserPort):
    """데모용 발급기. 1부터 순차 증가. 실 서비스 전환 시 키오스크 어댑터로 교체."""

    def __init__(self) -> None:
        self._counter = count(1)

    async def next_ticket(self) -> TicketNumber:
        return TicketNumber(next(self._counter))
