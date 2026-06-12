from __future__ import annotations

from datetime import datetime

from jb.apps.chat.app.ports.output.queue_registrar_port import QueueRegistrarPort
from jb.apps.chat.domain.entities.staff_handoff import StaffHandoff
from jb.apps.queue.app.dtos.queue_dto import RegisterQueueEntryCommand
from jb.apps.queue.app.ports.input.register_queue_entry_use_case import (
    RegisterQueueEntryUseCase,
)


class QueueRegistrarAdapter(QueueRegistrarPort):
    """핸드오프 표시 데이터를 스냅샷으로 queue 컨텍스트 등록 유스케이스에 위임한다.

    chat은 이 어댑터(adapter 레이어)에서만 queue를 알며, 도메인/앱은 포트에만 의존한다.
    """

    def __init__(self, register_use_case: RegisterQueueEntryUseCase) -> None:
        self._register = register_use_case

    async def register(self, handoff: StaffHandoff, created_at: datetime) -> None:
        briefing = handoff.briefing
        await self._register.execute(
            RegisterQueueEntryCommand(
                handoff_id=handoff.handoff_id,
                customer_name=handoff.customer.name,
                customer_age=handoff.customer.age,
                purpose=briefing.purpose,
                target=briefing.target,
                amount=briefing.amount,
                required_docs=briefing.required_docs,
                special_notes=briefing.special_notes,
                advice=briefing.advice,
                original_message=handoff.original_message,
                created_at=created_at,
            )
        )
