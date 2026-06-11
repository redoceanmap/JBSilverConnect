from __future__ import annotations

from abc import ABC, abstractmethod

from jb.core.customer.customer_profile import CustomerProfile
from jb.shared_kernel.value_objects import UserId


class CustomerDirectoryPort(ABC):
    """
    고객 신상 조회 추상화. 창구 전달(handoff)이 고객정보를 붙일 때 사용하는 Driven Port.
    구현은 Adapter(Mock / 실 고객DB)가 담당.
    """

    @abstractmethod
    async def get(self, user_id: UserId) -> CustomerProfile: ...
