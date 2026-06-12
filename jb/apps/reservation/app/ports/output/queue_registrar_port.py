from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from jb.apps.reservation.domain.entities.reservation_entity import Reservation


class QueueRegistrarPort(ABC):
    @abstractmethod
    async def register(
        self,
        reservation: Reservation,
        customer_name: str,
        customer_age: int,
        created_at: datetime,
        note_summary: str,
    ) -> None: ...

    @abstractmethod
    async def deregister(self, reservation_id: str) -> None:
        """예약 취소 시 어드민 대기열에서도 해당 항목을 제거한다."""
        ...
