from __future__ import annotations

from fastapi import APIRouter, Depends

from jb.apps.chat.adapter.inbound.api.schemas.chat_schema import (
    ChatReplyResponse,
    ChatRequest,
    HandoffCardResponse,
    HandoffRequest,
    HandoffResponse,
)
from jb.apps.chat.app.dtos.chat_dto import (
    ConverseCommand,
    HandoffCommand,
    StaffHandoffCardView,
    UtteranceInput,
)
from jb.apps.chat.app.ports.input.converse_use_case import ConverseUseCase
from jb.apps.chat.app.ports.input.handoff_use_case import HandoffUseCase
from jb.apps.chat.app.ports.input.list_handoffs_use_case import ListHandoffsUseCase
from jb.apps.chat.dependencies.chat_provider import (
    get_converse_use_case,
    get_handoff_use_case,
    get_list_handoffs_use_case,
)

chat_router = APIRouter(prefix="/chat", tags=["chat"])


def _to_history(body: ChatRequest) -> tuple[UtteranceInput, ...]:
    return tuple(
        UtteranceInput(role=message.role, text=message.text)
        for message in body.messages
    )


def _to_card_response(card: StaffHandoffCardView) -> HandoffCardResponse:
    return HandoffCardResponse(
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
    )


@chat_router.post("/message", response_model=ChatReplyResponse)
async def send_message(
    body: ChatRequest,
    usecase: ConverseUseCase = Depends(get_converse_use_case),
) -> ChatReplyResponse:
    view = await usecase.execute(ConverseCommand(history=_to_history(body)))
    return ChatReplyResponse(reply=view.reply)


@chat_router.post("/handoff", response_model=HandoffResponse)
async def hand_off(
    body: HandoffRequest,
    usecase: HandoffUseCase = Depends(get_handoff_use_case),
) -> HandoffResponse:
    view = await usecase.execute(
        HandoffCommand(user_id=body.user_id, history=_to_history(body))
    )
    return HandoffResponse(
        card=_to_card_response(view.card),
        confirm_message=view.confirm_message,
    )


@chat_router.get("/handoffs", response_model=list[HandoffCardResponse])
async def list_handoffs(
    usecase: ListHandoffsUseCase = Depends(get_list_handoffs_use_case),
) -> list[HandoffCardResponse]:
    cards = await usecase.execute()
    return [_to_card_response(card) for card in cards]
