from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.queue.app.dtos.queue_dto import QueueEntryCardView


class ListQueueEntriesUseCase(ABC):
    """Driving Port — 창구 단말에 띄울 대기열 카드 목록 조회 계약."""

    @abstractmethod
    async def execute(self) -> list[QueueEntryCardView]: ...
