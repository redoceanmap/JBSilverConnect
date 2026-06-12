from __future__ import annotations

from datetime import datetime, timezone

from jb.apps.queue.app.ports.input.call_entry_use_case import CallEntryUseCase
from jb.apps.queue.app.ports.output.queue_entry_repository_port import (
    QueueEntryRepositoryPort,
)


class CallEntryInteractor(CallEntryUseCase):
    """SRP: '현장대기 고객 호출'만 책임진다. 호출 시각을 기록해 1분 뒤 자동 삭제된다."""

    def __init__(self, repository: QueueEntryRepositoryPort) -> None:
        self._repository = repository

    async def execute(self, handoff_id: str) -> None:
        entry = await self._repository.get(handoff_id)
        if entry is None:
            raise ValueError("대기열 항목을 찾을 수 없습니다")
        entry.call(datetime.now(timezone.utc))
        await self._repository.save(entry)
