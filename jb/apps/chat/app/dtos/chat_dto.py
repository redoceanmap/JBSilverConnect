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
    history: tuple[UtteranceInput, ...]


@dataclass(frozen=True)
class StaffHandoffView:
    summary: str
    confirm_message: str
