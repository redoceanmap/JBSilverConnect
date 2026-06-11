from __future__ import annotations

from dataclasses import dataclass

from jb.apps.branch.domain.value_objects.branch_vo import (
    Distance,
    GeoCoordinate,
    WaitStatus,
)


@dataclass
class Branch:
    """지점 — Aggregate Root. 현재 위치 기준 거리·대기 현황을 함께 가진다."""

    name: str
    coordinate: GeoCoordinate
    distance: Distance
    wait_status: WaitStatus
