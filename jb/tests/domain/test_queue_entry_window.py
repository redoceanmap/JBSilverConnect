from __future__ import annotations

from datetime import datetime, timezone

from jb.apps.queue.domain.entities.queue_entry_entity import QueueEntry
from jb.shared_kernel.value_objects import WindowType

_NOW = datetime(2026, 6, 12, 9, 0, tzinfo=timezone.utc)


def _entry(window_type: WindowType) -> QueueEntry:
    return QueueEntry(
        handoff_id="h1",
        customer_name="김대표",
        customer_age=45,
        purpose="법인 통장 개설",
        target="사업자통장",
        amount="해당 없음",
        required_docs="사업자등록증·법인 인감증명",
        special_notes="—",
        advice="법인 서류 확인 필요",
        original_message="사업자통장 만들러 왔어요",
        created_at=_NOW,
        window_type=window_type,
    )


def test_일반_고객은_위치번호만_표기된다():
    entry = _entry(WindowType.GENERAL)
    assert entry.ticket_label(position=1) == "2"


def test_법인_고객은_B_접두로_구별_호출된다():
    entry = _entry(WindowType.CORPORATE)
    assert entry.ticket_label(position=1) == "B2"
    # 기존 정수 대기번호는 그대로 유지된다.
    assert entry.ticket_number(position=1) == 2


def test_기본값은_일반_창구다():
    entry = QueueEntry(
        handoff_id="h2",
        customer_name="홍길동",
        customer_age=30,
        purpose="통장 정리",
        target="입출금통장",
        amount="—",
        required_docs="신분증",
        special_notes="—",
        advice="—",
        original_message="통장 정리",
        created_at=_NOW,
    )
    assert entry.window_type is WindowType.GENERAL
    assert entry.ticket_label(position=0) == "1"
