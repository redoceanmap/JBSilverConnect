from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProposeSavingsCommand:
    user_id: str


@dataclass(frozen=True)
class SavingsProposalView:
    idle_amount: int
    monthly_interest: int
    rate: float
    ai_message: str
    agree_label: str
    reject_label: str
