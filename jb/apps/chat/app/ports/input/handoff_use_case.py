from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.chat.app.dtos.chat_dto import HandoffCommand, StaffHandoffView


class HandoffUseCase(ABC):
    """Driving Port — 대화를 은행 직원 전달용 요약으로 만드는 유스케이스 계약."""

    @abstractmethod
    async def execute(self, command: HandoffCommand) -> StaffHandoffView: ...
