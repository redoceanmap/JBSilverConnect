from __future__ import annotations

from jb.apps.queue.app.ports.input.confirm_arrival_use_case import ConfirmArrivalUseCase
from jb.apps.queue.app.ports.output.queue_entry_repository_port import (
    QueueEntryRepositoryPort,
)


class ConfirmArrivalInteractor(ConfirmArrivalUseCase):
    """SRP: '대기 → 현장대기 전환'만 책임진다."""

    def __init__(self, repository: QueueEntryRepositoryPort) -> None:
        self._repository = repository

    async def execute(self, handoff_id: str) -> None:
        entry = await self._repository.get(handoff_id)
        if entry is None:
            raise ValueError("대기열 항목을 찾을 수 없습니다")
        entry.confirm_arrival()
        await self._repository.save(entry)
