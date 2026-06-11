from __future__ import annotations

from dataclasses import dataclass

from jb.shared_kernel.domain_event import DomainEvent
from jb.shared_kernel.value_objects import Money, UserId


@dataclass(frozen=True)
class SavingsProposalAccepted(DomainEvent):
    """어르신이 명시적으로 동의했을 때만 발생하는 과거형 도메인 이벤트."""

    user_id: UserId
    amount: Money
