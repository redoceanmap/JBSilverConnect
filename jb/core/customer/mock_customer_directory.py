from __future__ import annotations

from jb.core.customer.customer_profile import CustomerProfile
from jb.core.ports.customer_directory_port import CustomerDirectoryPort
from jb.shared_kernel.value_objects import UserId


class MockCustomerDirectory(CustomerDirectoryPort):
    """
    해커톤 데모용 Mock 구현. 데모 어르신 한 명을 돌려준다.
    실 서비스 전환 시 CustomerDbDirectory로 교체 — 유스케이스 코드 변경 0 (DIP).
    """

    async def get(self, user_id: UserId) -> CustomerProfile:
        return CustomerProfile(name="김순자", age=72)
