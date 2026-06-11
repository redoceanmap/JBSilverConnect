from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.reservation.domain.entities.reservation_entity import Reservation
from jb.shared_kernel.value_objects import UserId


class ReservationRepositoryPort(ABC):
    """예약 저장소 추상화. 구현은 Adapter(인메모리 Mock / 실 DB)가 담당."""

    @abstractmethod
    async def save(self, reservation: Reservation) -> None: ...

    @abstractmethod
    async def get(self, reservation_id: str) -> Reservation | None: ...

    @abstractmethod
    async def list_by_user(self, user_id: UserId) -> list[Reservation]: ...

    @abstractmethod
    async def find_active(
        self, user_id: UserId, branch_name: str | None
    ) -> Reservation | None: ...
