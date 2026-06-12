from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from jb.apps.queue.domain.value_objects.queue_vo import QueueStatus

# 대기 30분 미도착 시 파기, 호출 1분 뒤 자동 삭제.
_WAIT_LIMIT = timedelta(minutes=30)
_CALL_LIMIT = timedelta(minutes=1)


@dataclass
class QueueEntry:
    """창구 대기열의 한 고객 — Aggregate Root.

    핸드오프와 1:1이며 handoff_id를 자연 식별자로 쓴다. 직원에게 보여줄 표시
    데이터는 발급 시점 스냅샷으로 받아 보관한다(읽기 모델). 대기번호·도착예상은
    대기열 내 위치에서 파생하므로 엔티티가 들고 있지 않다.
    """

    handoff_id: str
    customer_name: str
    customer_age: int
    purpose: str
    target: str
    amount: str
    required_docs: str
    special_notes: str
    advice: str
    original_message: str
    created_at: datetime
    status: QueueStatus = QueueStatus.WAITING
    called_at: datetime | None = None

    def confirm_arrival(self) -> None:
        """대기 → 현장대기. 대기 상태가 아니면 무시한다."""
        if self.status is not QueueStatus.WAITING:
            return
        self.status = QueueStatus.ON_SITE

    def call(self, now: datetime) -> None:
        """현장대기 → 호출. 현장대기가 아니면 무시한다."""
        if self.status is not QueueStatus.ON_SITE:
            return
        self.status = QueueStatus.CALLED
        self.called_at = now

    def is_expired(self, now: datetime) -> bool:
        """대기 30분 초과 또는 호출 1분 초과 시 파기 대상."""
        if self.status is QueueStatus.WAITING:
            return now - self.created_at >= _WAIT_LIMIT
        if self.status is QueueStatus.CALLED and self.called_at is not None:
            return now - self.called_at >= _CALL_LIMIT
        return False

    def remaining_seconds(self, now: datetime) -> int:
        """카운트다운용 잔여 초. 현장대기는 만료가 없어 0을 돌려준다."""
        if self.status is QueueStatus.WAITING:
            return _countdown(self.created_at, _WAIT_LIMIT, now)
        if self.status is QueueStatus.CALLED and self.called_at is not None:
            return _countdown(self.called_at, _CALL_LIMIT, now)
        return 0

    def ticket_number(self, position: int) -> int:
        """대기열 위치(0부터)를 대기번호로 환산한다."""
        return position + 1

    def eta_text(self, position: int) -> str:
        """앞선 대기 인원으로 도착 예상 시간을 안내한다."""
        return f"약 {(position + 1) * 5}분 후 도착"


def _countdown(start: datetime, limit: timedelta, now: datetime) -> int:
    remaining = (start + limit) - now
    return max(0, int(remaining.total_seconds()))
