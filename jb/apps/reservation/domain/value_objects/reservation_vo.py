from __future__ import annotations

import enum
from dataclasses import dataclass


class ReservationStatus(enum.Enum):
    """예약 번호표 상태. 취소된 번호표도 이력으로 보존된다."""

    ACTIVE = "active"
    CANCELED = "canceled"


@dataclass(frozen=True)
class TicketNumber:
    """번호표 값 객체. 1 이상. 불변."""

    value: int

    def __post_init__(self) -> None:
        if self.value < 1:
            raise ValueError("번호표 번호는 1 이상이어야 합니다")


@dataclass(frozen=True)
class Purpose:
    """방문 목적 값 객체. 빈 값 불가. 불변."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("방문 목적은 비어 있을 수 없습니다")
