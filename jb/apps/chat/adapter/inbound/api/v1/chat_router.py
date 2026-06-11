from __future__ import annotations

from fastapi import APIRouter, Depends

from jb.apps.chat.adapter.inbound.api.schemas.chat_schema import (
    ChatReplyResponse,
    ChatRequest,
    HandoffResponse,
)
from jb.apps.chat.app.dtos.chat_dto import (
    ConverseCommand,
    HandoffCommand,
    UtteranceInput,
)
from jb.apps.chat.app.ports.input.converse_use_case import ConverseUseCase
from jb.apps.chat.app.ports.input.handoff_use_case import HandoffUseCase
from jb.apps.chat.dependencies.chat_provider import (
    get_converse_use_case,
    get_handoff_use_case,
)

chat_router = APIRouter(prefix="/chat", tags=["chat"])


def _to_history(body: ChatRequest) -> tuple[UtteranceInput, ...]:
    return tuple(
        UtteranceInput(role=message.role, text=message.text)
        for message in body.messages
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
    body: ChatRequest,
    usecase: HandoffUseCase = Depends(get_handoff_use_case),
) -> HandoffResponse:
    view = await usecase.execute(HandoffCommand(history=_to_history(body)))
    return HandoffResponse(summary=view.summary, confirm_message=view.confirm_message)
