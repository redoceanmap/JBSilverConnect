from __future__ import annotations

from abc import ABC, abstractmethod

from jb.shared_kernel.value_objects import Money, UserId


class AccountQueryPort(ABC):
    """
    계좌 조회 추상화. savings·briefing·report 컨텍스트가 공유하는 Driven Port.
    구현은 Adapter(Mock / 실 오픈뱅킹)가 담당.
    """

    @abstractmethod
    async def get_balance(self, user_id: UserId) -> Money: ...

    @abstractmethod
    async def get_idle_balance(self, user_id: UserId) -> Money: ...
