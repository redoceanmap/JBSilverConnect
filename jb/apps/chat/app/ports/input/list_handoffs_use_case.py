from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.chat.app.dtos.chat_dto import StaffHandoffCardView


class ListHandoffsUseCase(ABC):
    """Driving Port — 창구 단말에 띄울 전달 카드 목록 조회 계약."""

    @abstractmethod
    async def execute(self) -> list[StaffHandoffCardView]: ...
