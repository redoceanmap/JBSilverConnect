from __future__ import annotations

from jb.apps.savings.app.dtos.savings_dto import ProposeSavingsCommand, SavingsProposalView
from jb.apps.savings.app.ports.input.propose_savings_use_case import ProposeSavingsUseCase
from jb.apps.savings.app.ports.output.savings_repository import SavingsRepositoryPort
from jb.apps.savings.domain.entities.savings_proposal_entity import SavingsProposal
from jb.apps.savings.domain.value_objects.savings_vo import InterestRate
from jb.core.ports.account_query_port import AccountQueryPort
from jb.core.ports.llm_port import LlmPort
from jb.shared_kernel.value_objects import UserId


class ProposeSavingsInteractor(ProposeSavingsUseCase):
    """
    SRP: '파킹통장 제안 생성'만 책임진다. 이체 실행은 별도 유스케이스.
    DIP: 구체 구현(GeminiAdapter, MockRepo)이 아닌 Port에만 의존.
    """

    def __init__(
        self,
        account_query: AccountQueryPort,
        llm: LlmPort,
        repository: SavingsRepositoryPort,
    ) -> None:
        self._account_query = account_query
        self._llm = llm
        self._repository = repository

    async def execute(self, command: ProposeSavingsCommand) -> SavingsProposalView:
        user_id = UserId(command.user_id)
        idle = await self._account_query.get_idle_balance(user_id)

        proposal = SavingsProposal(
            user_id=user_id,
            idle_amount=idle,
            rate=InterestRate(0.035),
        )
        monthly = proposal.expected_monthly_interest()

        message = await self._llm.generate(
            f"어르신께 {idle.amount}원을 비밀금고에 옮기면 "
            f"매달 {monthly.amount}원 이자가 생긴다고 친근하게 안내해줘"
        )

        await self._repository.save(proposal)

        return SavingsProposalView(
            idle_amount=idle.amount,
            monthly_interest=monthly.amount,
            rate=proposal.rate.as_percent(),
            ai_message=message,
            agree_label="나를 믿고 옮겨다오",
            reject_label="내버려 둬라",
        )
