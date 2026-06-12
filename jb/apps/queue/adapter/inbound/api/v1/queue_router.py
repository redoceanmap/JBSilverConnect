from __future__ import annotations

from fastapi import APIRouter, Depends

from jb.apps.queue.adapter.inbound.api.schemas.queue_schema import (
    QueueEntryCardResponse,
)
from jb.apps.queue.app.dtos.queue_dto import QueueEntryCardView
from jb.apps.queue.app.ports.input.call_entry_use_case import CallEntryUseCase
from jb.apps.queue.app.ports.input.confirm_arrival_use_case import ConfirmArrivalUseCase
from jb.apps.queue.app.ports.input.list_queue_entries_use_case import (
    ListQueueEntriesUseCase,
)
from jb.apps.queue.dependencies.queue_provider import (
    get_call_entry_use_case,
    get_confirm_arrival_use_case,
    get_list_queue_entries_use_case,
)

queue_router = APIRouter(prefix="/queue", tags=["queue"])


def _to_card_response(card: QueueEntryCardView) -> QueueEntryCardResponse:
    return QueueEntryCardResponse(
        handoff_id=card.handoff_id,
        customer_name=card.customer_name,
        customer_age=card.customer_age,
        ticket_number=card.ticket_number,
        eta_text=card.eta_text,
        purpose=card.purpose,
        target=card.target,
        amount=card.amount,
        required_docs=card.required_docs,
        special_notes=card.special_notes,
        advice=card.advice,
        original_message=card.original_message,
        status=card.status,
        remaining_seconds=card.remaining_seconds,
    )


@queue_router.get("/entries", response_model=list[QueueEntryCardResponse])
async def list_entries(
    usecase: ListQueueEntriesUseCase = Depends(get_list_queue_entries_use_case),
) -> list[QueueEntryCardResponse]:
    """창구(어드민)용 — 대기/현장대기/호출 카드를 등급 순서로 조회한다."""
    cards = await usecase.execute()
    return [_to_card_response(card) for card in cards]


@queue_router.post("/entries/{handoff_id}/arrive", status_code=204)
async def confirm_arrival(
    handoff_id: str,
    usecase: ConfirmArrivalUseCase = Depends(get_confirm_arrival_use_case),
) -> None:
    """대기 고객 도착 인증 → 현장대기로 전환."""
    await usecase.execute(handoff_id)


@queue_router.post("/entries/{handoff_id}/call", status_code=204)
async def call_entry(
    handoff_id: str,
    usecase: CallEntryUseCase = Depends(get_call_entry_use_case),
) -> None:
    """현장대기 고객 호출 → 1분 뒤 자동 삭제."""
    await usecase.execute(handoff_id)
