from __future__ import annotations

from jb.apps.chat.app.ports.output.handoff_store_port import HandoffStorePort
from jb.apps.chat.domain.entities.staff_handoff import StaffHandoff


class InMemoryHandoffStore(HandoffStorePort):
    """데모용 인메모리 전달함. 발급 순서를 그대로 보관해 대기번호로 쓴다.

    실 서비스 전환 시 DB·메시지큐 어댑터로 교체 — 유스케이스 코드 변경 0 (DIP).
    """

    def __init__(self) -> None:
        self._items: list[StaffHandoff] = []

    async def save(self, handoff: StaffHandoff) -> None:
        self._items.append(handoff)

    async def list_active(self) -> list[StaffHandoff]:
        return list(self._items)
