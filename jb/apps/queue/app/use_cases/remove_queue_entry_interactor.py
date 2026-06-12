from __future__ import annotations

from jb.apps.queue.app.ports.input.remove_queue_entry_use_case import (
    RemoveQueueEntryUseCase,
)
from jb.apps.queue.app.ports.output.queue_entry_repository_port import (
    QueueEntryRepositoryPort,
)


class RemoveQueueEntryInteractor(RemoveQueueEntryUseCase):
    """SRP: '대기열 항목 제거'만 책임진다. 없는 항목은 무시한다(멱등)."""

    def __init__(self, repository: QueueEntryRepositoryPort) -> None:
        self._repository = repository

    async def execute(self, handoff_id: str) -> None:
        await self._repository.remove(handoff_id)
