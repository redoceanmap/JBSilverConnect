from __future__ import annotations

from functools import lru_cache

from jb.apps.savings.adapter.outbound.mock.mock_savings_repository import MockSavingsRepository
from jb.apps.savings.app.ports.input.propose_savings_use_case import ProposeSavingsUseCase
from jb.apps.savings.app.ports.output.savings_repository import SavingsRepositoryPort
from jb.apps.savings.app.use_cases.propose_savings_interactor import ProposeSavingsInteractor
from jb.core.di import get_account_query, get_llm


@lru_cache
def _get_savings_repository() -> SavingsRepositoryPort:
    return MockSavingsRepository()


def get_propose_savings_use_case() -> ProposeSavingsUseCase:
    return ProposeSavingsInteractor(
        account_query=get_account_query(),
        llm=get_llm(),
        repository=_get_savings_repository(),
    )
