from __future__ import annotations

from jb.apps.savings.app.dtos.savings_dto import ProposeSavingsCommand
from jb.apps.savings.app.ports.output.savings_repository import SavingsRepositoryPort
from jb.apps.savings.app.use_cases.propose_savings_interactor import ProposeSavingsInteractor
from jb.apps.savings.domain.entities.savings_proposal_entity import SavingsProposal
from jb.core.ports.account_query_port import AccountQueryPort
from jb.core.ports.llm_port import LlmPort
from jb.shared_kernel.value_objects import Money, UserId


class FakeLlm(LlmPort):
    async def generate(self, prompt: str) -> str:
        return "테스트 안내 문구"


class FakeAccountQuery(AccountQueryPort):
    async def get_balance(self, user_id: UserId) -> Money:
        return Money(1_200_000)

    async def get_idle_balance(self, user_id: UserId) -> Money:
        return Money(50_000)


class FakeSavingsRepository(SavingsRepositoryPort):
    def __init__(self) -> None:
        self.saved: SavingsProposal | None = None

    async def save(self, proposal: SavingsProposal) -> None:
        self.saved = proposal

    async def find_by_user(self, user_id: UserId) -> SavingsProposal | None:
        return self.saved


async def test_제안_생성_유스케이스():
    repository = FakeSavingsRepository()
    usecase = ProposeSavingsInteractor(FakeAccountQuery(), FakeLlm(), repository)

    view = await usecase.execute(ProposeSavingsCommand("u1"))

    assert view.idle_amount == 50_000
    assert view.monthly_interest == 145  # 50000 * 0.035 / 12
    assert view.rate == 3.5
    assert view.ai_message == "테스트 안내 문구"
    assert repository.saved is not None  # 제안이 영속화됨
