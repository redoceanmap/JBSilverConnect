from __future__ import annotations

from datetime import datetime

from jb.apps.queue.app.dtos.queue_dto import RegisterQueueEntryCommand
from jb.apps.queue.app.ports.input.register_queue_entry_use_case import (
    RegisterQueueEntryUseCase,
)
from jb.apps.queue.app.ports.input.remove_queue_entry_use_case import (
    RemoveQueueEntryUseCase,
)
from jb.apps.reservation.app.ports.output.queue_registrar_port import QueueRegistrarPort
from jb.apps.reservation.domain.entities.reservation_entity import Reservation


class ReservationQueueRegistrarAdapter(QueueRegistrarPort):
    def __init__(
        self,
        register_use_case: RegisterQueueEntryUseCase,
        remove_use_case: RemoveQueueEntryUseCase,
    ) -> None:
        self._register = register_use_case
        self._remove = remove_use_case

    async def register(
        self,
        reservation: Reservation,
        customer_name: str,
        customer_age: int,
        created_at: datetime,
        note_summary: str,
    ) -> None:
        await self._register.execute(
            RegisterQueueEntryCommand(
                handoff_id=reservation.reservation_id,
                customer_name=customer_name,
                customer_age=customer_age,
                purpose=reservation.purpose.value,
                target="",
                amount="",
                required_docs="",
                special_notes=note_summary,
                advice="",
                original_message=reservation.note or "",
                created_at=created_at,
                window_type=reservation.window_type.code,
            )
        )

    async def deregister(self, reservation_id: str) -> None:
        await self._remove.execute(reservation_id)
