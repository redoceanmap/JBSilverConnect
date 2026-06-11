from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.savings.domain.entities.savings_proposal_entity import SavingsProposal
from jb.shared_kernel.value_objects import UserId


class SavingsRepositoryPort(ABC):
    """도메인이 정의하는 영속성 계약. 구현은 Adapter가 담당. Aggregate 단위로만."""

    @abstractmethod
    async def save(self, proposal: SavingsProposal) -> None: ...

    @abstractmethod
    async def find_by_user(self, user_id: UserId) -> SavingsProposal | None: ...
