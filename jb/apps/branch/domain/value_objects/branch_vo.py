from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GeoCoordinate:
    """위경도 좌표 값 객체. 불변."""

    latitude: float
    longitude: float


@dataclass(frozen=True)
class Distance:
    """거리 값 객체. 미터 단위. 음수 불가. 불변."""

    meters: int

    def __post_init__(self) -> None:
        if self.meters < 0:
            raise ValueError("거리는 음수일 수 없습니다")

    def as_km(self) -> float:
        return round(self.meters / 1000, 2)


@dataclass(frozen=True)
class WaitStatus:
    """창구 대기 현황 값 객체. 음수 불가. 불변."""

    waiting_count: int

    def __post_init__(self) -> None:
        if self.waiting_count < 0:
            raise ValueError("대기 인원은 음수일 수 없습니다")
