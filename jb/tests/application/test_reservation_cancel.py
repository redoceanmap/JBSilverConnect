from __future__ import annotations

import pytest

from jb.apps.queue.adapter.outbound.mock.in_memory_queue_repository import (
    InMemoryQueueRepository,
)
from jb.apps.queue.app.use_cases.register_queue_entry_interactor import (
    RegisterQueueEntryInteractor,
)
from jb.apps.queue.app.use_cases.remove_queue_entry_interactor import (
    RemoveQueueEntryInteractor,
)
from jb.apps.reservation.adapter.outbound.mock.in_memory_reservation_repository import (
    InMemoryReservationRepository,
)
from jb.apps.reservation.adapter.outbound.mock.mock_ticket_dispenser import (
    MockTicketDispenser,
)
from jb.apps.reservation.adapter.outbound.queue.reservation_queue_registrar_adapter import (
    ReservationQueueRegistrarAdapter,
)
from jb.apps.reservation.app.dtos.reservation_dto import (
    CancelReservationCommand,
    CreateReservationCommand,
)
from jb.apps.reservation.app.use_cases.cancel_reservation_interactor import (
    CancelReservationInteractor,
)
from jb.apps.reservation.app.use_cases.create_reservation_interactor import (
    CreateReservationInteractor,
)
from jb.core.customer.mock_customer_directory import MockCustomerDirectory
from jb.core.ports.llm_port import LlmPort


class _StubLlm(LlmPort):
    async def generate(self, prompt: str) -> str:
        return "요약된 메모"


def _wiring():
    queue_repo = InMemoryQueueRepository()
    registrar = ReservationQueueRegistrarAdapter(
        RegisterQueueEntryInteractor(queue_repo),
        RemoveQueueEntryInteractor(queue_repo),
    )
    reservation_repo = InMemoryReservationRepository()
    create = CreateReservationInteractor(
        dispenser=MockTicketDispenser(),
        repository=reservation_repo,
        customer_directory=MockCustomerDirectory(),
        queue_registrar=registrar,
        llm=_StubLlm(),
    )
    cancel = CancelReservationInteractor(
        repository=reservation_repo,
        queue_registrar=registrar,
    )
    return queue_repo, create, cancel


@pytest.mark.asyncio
async def test_예약_취소시_어드민_대기열에서도_제거된다():
    queue_repo, create, cancel = _wiring()

    view = await create.execute(
        CreateReservationCommand(
            user_id="user_kim_sonja", purpose="통장 정리", branch_name="전북은행 본점"
        )
    )
    rid = view.reservation_id
    assert await queue_repo.get(rid) is not None  # 발급 시 대기열에 등록

    cancelled = await cancel.execute(CancelReservationCommand(reservation_id=rid))
    assert cancelled.status == "canceled"
    assert await queue_repo.get(rid) is None  # 취소 시 대기열에서 제거


@pytest.mark.asyncio
async def test_창구_전달_메모는_AI_요약으로_특이사항에_원문은_그대로_남는다():
    queue_repo, create, _ = _wiring()

    raw_note = "부동산 대출 관련 부동산 부동산 대출 부동산 대추루루룰루" * 5
    view = await create.execute(
        CreateReservationCommand(
            user_id="user_kim_sonja",
            purpose="카드 발급",
            branch_name="전북은행 본점",
            note=raw_note,
        )
    )

    entry = await queue_repo.get(view.reservation_id)
    assert entry.special_notes == "요약된 메모"  # 특이사항 = AI 요약
    assert entry.original_message == raw_note  # 원문 = 입력 그대로
