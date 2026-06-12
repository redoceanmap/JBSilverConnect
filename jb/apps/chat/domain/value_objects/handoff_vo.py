from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VisitBriefing:
    """AI가 정리한 창구 방문 안내. 직원이 한눈에 보는 구조화 필드. 불변."""

    purpose: str
    target: str
    amount: str
    required_docs: str
    special_notes: str
    advice: str
    window_type: str = "general"
