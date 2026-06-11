from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.savings.app.dtos.savings_dto import ProposeSavingsCommand, SavingsProposalView


class ProposeSavingsUseCase(ABC):
    """Driving Port — 외부(라우터)가 호출하는 유스케이스 계약."""

    @abstractmethod
    async def execute(self, command: ProposeSavingsCommand) -> SavingsProposalView: ...
