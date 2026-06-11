from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DomainEvent:
    """도메인 이벤트 베이스. 불변. 과거형으로 명명한다 (예: SavingsProposalAccepted)."""
