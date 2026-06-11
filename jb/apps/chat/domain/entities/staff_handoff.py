from __future__ import annotations

from dataclasses import dataclass

from jb.apps.chat.domain.value_objects.handoff_vo import VisitBriefing
from jb.core.customer.customer_profile import CustomerProfile


@dataclass
class StaffHandoff:
    """창구 단말로 전달된 한 건의 방문 안내 — Aggregate Root.

    대기번호·도착 예상은 창구 대기열 내 위치에서 파생되므로 엔티티가 들고 있지 않다.
    """

    handoff_id: str
    customer: CustomerProfile
    briefing: VisitBriefing
    original_message: str

    def ticket_number(self, queue_position: int) -> int:
        """대기열 위치(0부터)를 대기번호로 환산한다."""
        return queue_position + 1

    def eta_text(self, queue_position: int) -> str:
        """앞선 대기 인원으로 도착 예상 시간을 안내한다."""
        return f"약 {(queue_position + 1) * 5}분 후 도착"
