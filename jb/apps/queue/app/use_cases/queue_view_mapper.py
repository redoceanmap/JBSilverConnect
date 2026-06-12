from __future__ import annotations

from datetime import datetime

from jb.apps.queue.app.dtos.queue_dto import QueueEntryCardView
from jb.apps.queue.domain.entities.queue_entry_entity import QueueEntry


def to_card(entry: QueueEntry, position: int, now: datetime) -> QueueEntryCardView:
    """대기열 엔트리를 창구 카드 뷰로 변환한다. 대기번호·도착예상은 위치에서 파생."""
    return QueueEntryCardView(
        handoff_id=entry.handoff_id,
        customer_name=entry.customer_name,
        customer_age=entry.customer_age,
        ticket_number=entry.ticket_number(position),
        eta_text=entry.eta_text(position),
        purpose=entry.purpose,
        target=entry.target,
        amount=entry.amount,
        required_docs=entry.required_docs,
        special_notes=entry.special_notes,
        advice=entry.advice,
        original_message=entry.original_message,
        status=entry.status.value,
        remaining_seconds=entry.remaining_seconds(now),
    )
