from __future__ import annotations

from abc import ABC, abstractmethod


class RemoveQueueEntryUseCase(ABC):
    """Driving Port — 대기열에서 항목을 제거하는 계약(예: 예약 취소 시 어드민 단말에서 삭제)."""

    @abstractmethod
    async def execute(self, handoff_id: str) -> None: ...
