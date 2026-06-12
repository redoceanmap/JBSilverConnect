from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.chat.app.dtos.chat_dto import ChatReplyView, ConverseCommand


class ConverseUseCase(ABC):
    """Driving Port — 고객님의 말에 도우미가 응답하는 유스케이스 계약."""

    @abstractmethod
    async def execute(self, command: ConverseCommand) -> ChatReplyView: ...
