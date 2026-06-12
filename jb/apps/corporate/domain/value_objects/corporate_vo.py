from __future__ import annotations

import math
from dataclasses import dataclass

_EARTH_RADIUS_M = 6_371_000


@dataclass(frozen=True)
class GeoPoint:
    """위경도 좌표 값 객체. 불변."""

    latitude: float
    longitude: float

    def distance_meters_to(self, other: "GeoPoint") -> int:
        """두 좌표 사이 대략 거리(m). 짧은 거리에 충분한 등거리 근사."""
        mean_lat = math.radians((self.latitude + other.latitude) / 2)
        dx = math.radians(other.longitude - self.longitude) * math.cos(mean_lat)
        dy = math.radians(other.latitude - self.latitude)
        return int(_EARTH_RADIUS_M * math.hypot(dx, dy))


@dataclass(frozen=True)
class IssuingInstitution:
    """필요 서류를 발급·접수하는 기관과 사용자 위치 기준 거리. 불변."""

    name: str
    kind: str
    distance_meters: int


@dataclass(frozen=True)
class CorporateTaskGuide:
    """법인 사무 한 건의 안내 — 필요 서류·예상 비용·발급 기관(가까운 순). 불변."""

    task_name: str
    required_docs: tuple[str, ...]
    estimated_cost: str
    institutions: tuple[IssuingInstitution, ...]
