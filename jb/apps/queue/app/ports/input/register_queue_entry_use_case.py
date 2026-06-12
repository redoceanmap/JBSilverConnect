from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.queue.app.dtos.queue_dto import RegisterQueueEntryCommand


class RegisterQueueEntryUseCase(ABC):
    """Driving Port — 핸드오프를 창구 대기열에 등록하는 계약."""

    @abstractmethod
    async def execute(self, command: RegisterQueueEntryCommand) -> None: ...
