from __future__ import annotations

from datetime import datetime, timedelta, timezone

from jb.apps.queue.domain.entities.queue_entry_entity import QueueEntry
from jb.apps.queue.domain.value_objects.queue_vo import QueueStatus

_NOW = datetime(2026, 6, 12, 9, 0, tzinfo=timezone.utc)


def _entry(created_at: datetime = _NOW) -> QueueEntry:
    return QueueEntry(
        handoff_id="h1",
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


def test_발급_직후는_대기_상태이고_30분_잔여():
    entry = _entry()
    assert entry.status is QueueStatus.WAITING
    assert entry.remaining_seconds(_NOW) == 30 * 60


def test_도착인증하면_현장대기로_전환되고_만료가_없다():
    entry = _entry()
    entry.confirm_arrival()
    assert entry.status is QueueStatus.ON_SITE
    assert entry.is_expired(_NOW + timedelta(hours=1)) is False
    assert entry.remaining_seconds(_NOW) == 0


def test_현장대기가_아니면_호출은_무시된다():
    entry = _entry()
    entry.call(_NOW)  # 대기 상태에서 호출 시도
    assert entry.status is QueueStatus.WAITING


def test_호출하면_1분_뒤_만료된다():
    entry = _entry()
    entry.confirm_arrival()
    entry.call(_NOW)
    assert entry.status is QueueStatus.CALLED
    assert entry.remaining_seconds(_NOW) == 60
    assert entry.is_expired(_NOW + timedelta(seconds=59)) is False
    assert entry.is_expired(_NOW + timedelta(seconds=60)) is True


def test_대기_30분_초과하면_만료된다():
    entry = _entry()
    assert entry.is_expired(_NOW + timedelta(minutes=29, seconds=59)) is False
    assert entry.is_expired(_NOW + timedelta(minutes=30)) is True


def test_잔여초는_음수가_되지_않는다():
    entry = _entry()
    assert entry.remaining_seconds(_NOW + timedelta(hours=2)) == 0
