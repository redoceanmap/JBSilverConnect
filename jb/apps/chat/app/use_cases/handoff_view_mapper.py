from __future__ import annotations

from jb.apps.chat.app.dtos.chat_dto import StaffHandoffCardView
from jb.apps.chat.domain.entities.staff_handoff import StaffHandoff


def to_card(handoff: StaffHandoff, queue_position: int) -> StaffHandoffCardView:
    """전달 엔티티를 창구 단말 카드 뷰로 변환한다. 대기번호·도착예상은 위치에서 파생."""
    briefing = handoff.briefing
    return StaffHandoffCardView(
        handoff_id=handoff.handoff_id,
        customer_name=handoff.customer.name,
        customer_age=handoff.customer.age,
        ticket_number=handoff.ticket_number(queue_position),
        eta_text=handoff.eta_text(queue_position),
        purpose=briefing.purpose,
        target=briefing.target,
        amount=briefing.amount,
        required_docs=briefing.required_docs,
        special_notes=briefing.special_notes,
        advice=briefing.advice,
        original_message=handoff.original_message,
    )
