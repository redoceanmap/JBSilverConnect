from __future__ import annotations

from jb.apps.reservation.app.ports.output.reservation_repository_port import (
    ReservationRepositoryPort,
)
from jb.apps.reservation.domain.entities.reservation_entity import Reservation
from jb.apps.reservation.domain.value_objects.reservation_vo import ReservationStatus
from jb.shared_kernel.value_objects import UserId


class InMemoryReservationRepository(ReservationRepositoryPort):
    """데모용 인메모리 저장소. ID로 upsert해 발권 이력을 보관. 실 서비스 전환 시 DB 어댑터로 교체."""

    def __init__(self) -> None:
        self._store: dict[str, Reservation] = {}

    async def save(self, reservation: Reservation) -> None:
        self._store[reservation.reservation_id] = reservation

    async def get(self, reservation_id: str) -> Reservation | None:
        return self._store.get(reservation_id)

    async def list_by_user(self, user_id: UserId) -> list[Reservation]:
        return [r for r in self._store.values() if r.user_id == user_id]

    async def list_active_all(self) -> list[Reservation]:
        return [
            r for r in self._store.values() if r.status == ReservationStatus.ACTIVE
        ]

    async def find_active(
        self, user_id: UserId, branch_name: str | None
    ) -> Reservation | None:
        for reservation in self._store.values():
            if (
                reservation.user_id == user_id
                and reservation.branch_name == branch_name
                and reservation.status == ReservationStatus.ACTIVE
            ):
                return reservation
        return None
