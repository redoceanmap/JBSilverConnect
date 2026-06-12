from __future__ import annotations

from datetime import datetime, timezone

from jb.apps.queue.app.dtos.queue_dto import QueueEntryCardView
from jb.apps.queue.app.ports.input.list_queue_entries_use_case import (
    ListQueueEntriesUseCase,
)
from jb.apps.queue.app.ports.output.queue_entry_repository_port import (
    QueueEntryRepositoryPort,
)
from jb.apps.queue.app.use_cases.queue_view_mapper import to_card


class ListQueueEntriesInteractor(ListQueueEntriesUseCase):
    """SRP: '대기열 카드 목록 조회 + 만료 항목 자동 파기'만 책임진다."""

    def __init__(self, repository: QueueEntryRepositoryPort) -> None:
        self._repository = repository

    async def execute(self) -> list[QueueEntryCardView]:
        now = datetime.now(timezone.utc)
        entries = await self._repository.list_active()

        active = []
        for entry in entries:
            if entry.is_expired(now):
                await self._repository.remove(entry.handoff_id)
                continue
            active.append(entry)

        return [to_card(entry, position, now) for position, entry in enumerate(active)]
