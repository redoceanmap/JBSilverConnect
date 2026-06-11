from __future__ import annotations

from jb.apps.chat.app.dtos.chat_dto import StaffHandoffCardView
from jb.apps.chat.app.ports.input.list_handoffs_use_case import ListHandoffsUseCase
from jb.apps.chat.app.ports.output.handoff_store_port import HandoffStorePort
from jb.apps.chat.app.use_cases.handoff_view_mapper import to_card


class ListHandoffsInteractor(ListHandoffsUseCase):
    """SRP: 창구 단말용 전달 카드 목록(발급 순서) 조회만 책임진다. DIP: 전달함 Port에만 의존."""

    def __init__(self, store: HandoffStorePort) -> None:
        self._store = store

    async def execute(self) -> list[StaffHandoffCardView]:
        items = await self._store.list_active()
        return [to_card(handoff, position) for position, handoff in enumerate(items)]
