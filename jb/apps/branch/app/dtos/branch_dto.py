from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FindNearbyBranchesCommand:
    latitude: float
    longitude: float
    limit: int = 3


@dataclass(frozen=True)
class BranchView:
    name: str
    distance_meters: int
    waiting_count: int
