from __future__ import annotations

from jb.apps.savings.app.ports.output.savings_repository import SavingsRepositoryPort
from jb.apps.savings.domain.entities.savings_proposal_entity import SavingsProposal
from jb.shared_kernel.value_objects import UserId


class MockSavingsRepository(SavingsRepositoryPort):
    """
    데모용 in-memory 구현. 실 서비스 전환 시 SupabaseSavingsRepository로 교체 — 유스케이스 변경 0.
    내부 저장소는 사용자별 Aggregate 인덱스(타입 보존: 값은 SavingsProposal 엔티티).
    """

    def __init__(self) -> None:
        self._store: dict[str, SavingsProposal] = {}

    async def save(self, proposal: SavingsProposal) -> None:
        self._store[proposal.user_id.value] = proposal

    async def find_by_user(self, user_id: UserId) -> SavingsProposal | None:
        return self._store.get(user_id.value)
