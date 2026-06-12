from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from jb.apps.reservation.app.dtos.reservation_dto import (
    CreateReservationCommand,
    ReservationView,
)
from jb.apps.reservation.app.ports.input.create_reservation_use_case import (
    CreateReservationUseCase,
)
from jb.apps.reservation.app.ports.output.queue_registrar_port import QueueRegistrarPort
from jb.apps.reservation.app.ports.output.reservation_repository_port import (
    ReservationRepositoryPort,
)
from jb.apps.reservation.app.ports.output.ticket_dispenser_port import TicketDispenserPort
from jb.apps.reservation.app.use_cases.reservation_view_mapper import to_view
from jb.apps.reservation.domain.entities.reservation_entity import Reservation
from jb.apps.reservation.domain.value_objects.reservation_vo import Purpose
from jb.core.ports.customer_directory_port import CustomerDirectoryPort
from jb.core.ports.llm_port import LlmPort
from jb.shared_kernel.value_objects import UserId, window_type_from_code

_SUMMARY_INSTRUCTION = (
    "다음은 은행 방문 고객이 창구 직원에게 전달하려고 남긴 메모다. "
    "직원이 한눈에 파악하도록 핵심만 간결한 한 문장으로 요약해라. "
    "요약문만 출력하고 다른 말이나 따옴표는 붙이지 마라.\n\n[메모]\n"
)


class CreateReservationInteractor(CreateReservationUseCase):
    """SRP: '예약 생성 + 번호표 발권'만 책임진다. DIP: 발급기·저장소·LLM Port에만 의존."""

    def __init__(
        self,
        dispenser: TicketDispenserPort,
        repository: ReservationRepositoryPort,
        customer_directory: CustomerDirectoryPort,
        queue_registrar: QueueRegistrarPort,
        llm: LlmPort,
    ) -> None:
        self._dispenser = dispenser
        self._repository = repository
        self._customer_directory = customer_directory
        self._queue_registrar = queue_registrar
        self._llm = llm

    async def execute(self, command: CreateReservationCommand) -> ReservationView:
        user_id = UserId(command.user_id)

        # 같은 지점에 이미 활성 번호표가 있으면 중복 발권하지 않고 그대로 돌려준다.
        existing = await self._repository.find_active(user_id, command.branch_name)
        if existing is not None:
            return to_view(existing)

        ticket = await self._dispenser.next_ticket()
        reservation = Reservation(
            reservation_id=uuid4().hex,
            user_id=user_id,
            purpose=Purpose(command.purpose),
            ticket=ticket,
            branch_name=command.branch_name,
            note=command.note,
            window_type=window_type_from_code(command.window_type),
        )
        await self._repository.save(reservation)

        customer = await self._customer_directory.get(user_id)
        note_summary = await self._summarize_note(command.note)
        await self._queue_registrar.register(
            reservation,
            customer.name,
            customer.age,
            datetime.now(timezone.utc),
            note_summary,
        )

        return to_view(reservation)

    async def _summarize_note(self, note: str | None) -> str:
        """창구 전달 메모를 직원이 보기 쉽게 한 문장으로 AI 요약한다. 메모가 없으면 빈 값."""
        text = (note or "").strip()
        if not text:
            return ""
        summary = await self._llm.generate(f"{_SUMMARY_INSTRUCTION}{text}")
        return summary.strip()
