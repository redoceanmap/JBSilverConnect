from __future__ import annotations

from jb.core.ports.account_query_port import AccountQueryPort
from jb.shared_kernel.value_objects import Money, UserId


class MockAccountQuery(AccountQueryPort):
    """
    해커톤 데모용 Mock 구현.
    실 서비스 전환 시 OpenBankingAccountQuery로 교체 — 유스케이스 코드 변경 0 (DIP).
    """

    async def get_balance(self, user_id: UserId) -> Money:
        return Money(1_200_000)

    async def get_idle_balance(self, user_id: UserId) -> Money:
        return Money(50_000)
