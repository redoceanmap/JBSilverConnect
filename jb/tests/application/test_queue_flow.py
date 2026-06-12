from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from jb.apps.queue.adapter.outbound.mock.in_memory_queue_repository import (
    InMemoryQueueRepository,
)
from jb.apps.queue.app.dtos.queue_dto import RegisterQueueEntryCommand
from jb.apps.queue.app.use_cases.call_entry_interactor import CallEntryInteractor
from jb.apps.queue.app.use_cases.confirm_arrival_interactor import (
    ConfirmArrivalInteractor,
)
from jb.apps.queue.app.use_cases.list_queue_entries_interactor import (
    ListQueueEntriesInteractor,
)
from jb.apps.queue.app.use_cases.register_queue_entry_interactor import (
    RegisterQueueEntryInteractor,
)


def _command(handoff_id: str, created_at: datetime) -> RegisterQueueEntryCommand:
    return RegisterQueueEntryCommand(
        handoff_id=handoff_id,
        customer_name="김선자",
        customer_age=86,
        purpose="통장 정리",
        target="입출금통장",
        amount="5만원",
        required_docs="통장·신분증",
        special_notes="천천히",
        advice="미리 준비",
        original_message="통장 정리하러 왔어요",
        created_at=created_at,
    )


@pytest.mark.asyncio
async def test_등록_도착인증_호출_흐름():
    repo = InMemoryQueueRepository()
    register = RegisterQueueEntryInteractor(repo)
    arrive = ConfirmArrivalInteractor(repo)
    call = CallEntryInteractor(repo)
    listing = ListQueueEntriesInteractor(repo)

    now = datetime.now(timezone.utc)
    await register.execute(_command("h1", now))
    await register.execute(_command("h2", now))

    cards = await listing.execute()
    assert [c.ticket_number for c in cards] == [1, 2]
    assert all(c.status == "waiting" for c in cards)

    await arrive.execute("h1")
    cards = await listing.execute()
    assert next(c.status for c in cards if c.handoff_id == "h1") == "on_site"

    await call.execute("h1")
    cards = await listing.execute()
    assert next(c.status for c in cards if c.handoff_id == "h1") == "called"


@pytest.mark.asyncio
async def test_만료_항목은_조회_시_자동_파기된다():
    repo = InMemoryQueueRepository()
    register = RegisterQueueEntryInteractor(repo)
    listing = ListQueueEntriesInteractor(repo)

    old = datetime.now(timezone.utc) - timedelta(minutes=31)
    fresh = datetime.now(timezone.utc)
    await register.execute(_command("old", old))
    await register.execute(_command("fresh", fresh))

    cards = await listing.execute()
    assert [c.handoff_id for c in cards] == ["fresh"]
    assert await repo.get("old") is None


@pytest.mark.asyncio
async def test_없는_항목_도착인증은_오류():
    repo = InMemoryQueueRepository()
    arrive = ConfirmArrivalInteractor(repo)
    with pytest.raises(ValueError):
        await arrive.execute("nope")
