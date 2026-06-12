from __future__ import annotations

from jb.apps.queue.app.ports.output.queue_entry_repository_port import (
    QueueEntryRepositoryPort,
)
from jb.apps.queue.domain.entities.queue_entry_entity import QueueEntry


class InMemoryQueueRepository(QueueEntryRepositoryPort):
    """데모용 인메모리 대기열 저장소. dict는 등록 순서를 보존해 대기번호로 쓴다.

    실 서비스 전환 시 DB·키오스크 어댑터로 교체 — 유스케이스 코드 변경 0 (DIP).
    """

    def __init__(self) -> None:
        self._store: dict[str, QueueEntry] = {}

    async def save(self, entry: QueueEntry) -> None:
        self._store[entry.handoff_id] = entry

    async def get(self, handoff_id: str) -> QueueEntry | None:
        return self._store.get(handoff_id)

    async def remove(self, handoff_id: str) -> None:
        self._store.pop(handoff_id, None)

    async def list_active(self) -> list[QueueEntry]:
        return list(self._store.values())
