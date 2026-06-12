from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CorporateGuideQuery:
    user_id: str
    latitude: float
    longitude: float
    topic: str = "corporate"


@dataclass(frozen=True)
class InstitutionView:
    name: str
    kind: str
    distance_meters: int


@dataclass(frozen=True)
class CorporateTaskView:
    task_name: str
    required_docs: tuple[str, ...]
    estimated_cost: str
    institutions: tuple[InstitutionView, ...]


@dataclass(frozen=True)
class CorporateGuideView:
    message: str
    tasks: tuple[CorporateTaskView, ...]
