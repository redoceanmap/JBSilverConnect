from __future__ import annotations

from jb.apps.queue.app.dtos.queue_dto import RegisterQueueEntryCommand
from jb.apps.queue.app.ports.input.register_queue_entry_use_case import (
    RegisterQueueEntryUseCase,
)
from jb.apps.queue.app.ports.output.queue_entry_repository_port import (
    QueueEntryRepositoryPort,
)
from jb.apps.queue.domain.entities.queue_entry_entity import QueueEntry


class RegisterQueueEntryInteractor(RegisterQueueEntryUseCase):
    """SRP: '핸드오프 스냅샷을 대기열 엔트리로 등록'만 책임진다."""

    def __init__(self, repository: QueueEntryRepositoryPort) -> None:
        self._repository = repository

    async def execute(self, command: RegisterQueueEntryCommand) -> None:
        entry = QueueEntry(
            handoff_id=command.handoff_id,
            customer_name=command.customer_name,
            customer_age=command.customer_age,
            purpose=command.purpose,
            target=command.target,
            amount=command.amount,
            required_docs=command.required_docs,
            special_notes=command.special_notes,
            advice=command.advice,
            original_message=command.original_message,
            created_at=command.created_at,
        )
        await self._repository.save(entry)
