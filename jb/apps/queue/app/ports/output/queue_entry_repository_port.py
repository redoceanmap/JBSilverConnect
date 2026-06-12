from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.queue.domain.entities.queue_entry_entity import QueueEntry


class QueueEntryRepositoryPort(ABC):
    """대기열 저장소 추상화 — Driven Port. 등록 순서를 유지한다."""

    @abstractmethod
    async def save(self, entry: QueueEntry) -> None: ...

    @abstractmethod
    async def get(self, handoff_id: str) -> QueueEntry | None: ...

    @abstractmethod
    async def remove(self, handoff_id: str) -> None: ...

    @abstractmethod
    async def list_active(self) -> list[QueueEntry]: ...
