from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.reservation.domain.value_objects.reservation_vo import TicketNumber


class TicketDispenserPort(ABC):
    """번호표 발급기 추상화. 구현은 Adapter(Mock / 실 키오스크 연동)가 담당."""

    @abstractmethod
    async def next_ticket(self) -> TicketNumber: ...
