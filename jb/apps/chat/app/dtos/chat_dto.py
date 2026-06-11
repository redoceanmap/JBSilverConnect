from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UtteranceInput:
    """라우터가 넘기는 입력 발화. role은 'user'/'assistant'."""

    role: str
    text: str


@dataclass(frozen=True)
class ConverseCommand:
    history: tuple[UtteranceInput, ...]


@dataclass(frozen=True)
class ChatReplyView:
    reply: str


@dataclass(frozen=True)
class HandoffCommand:
    user_id: str
    history: tuple[UtteranceInput, ...]


@dataclass(frozen=True)
class StaffHandoffCardView:
    """창구 단말에 뜨는 전달 카드 한 건."""

    handoff_id: str
    customer_name: str
    customer_age: int
    ticket_number: int
    eta_text: str
    purpose: str
    target: str
    amount: str
    required_docs: str
    special_notes: str
    advice: str
    original_message: str


@dataclass(frozen=True)
class StaffHandoffView:
    """전달 직후 어르신에게 돌려줄 응답 — 카드 + 안심 메시지."""

    card: StaffHandoffCardView
    confirm_message: str
