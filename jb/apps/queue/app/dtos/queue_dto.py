from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RegisterQueueEntryCommand:
    """핸드오프 발급 시 대기열에 올릴 표시 스냅샷 + 발급 시각."""

    handoff_id: str
    customer_name: str
    customer_age: int
    purpose: str
    target: str
    amount: str
    required_docs: str
    special_notes: str
    advice: str
    original_message: str
    created_at: datetime
    window_type: str = "general"


@dataclass(frozen=True)
class QueueEntryCardView:
    """창구 단말에 뜨는 대기열 카드 한 건."""

    handoff_id: str
    customer_name: str
    customer_age: int
    ticket_number: int
    ticket_label: str
    window_type: str
    eta_text: str
    purpose: str
    target: str
    amount: str
    required_docs: str
    special_notes: str
    advice: str
    original_message: str
    status: str
    remaining_seconds: int
