from __future__ import annotations

from jb.core.customer.customer_profile import CustomerProfile
from jb.core.ports.customer_directory_port import CustomerDirectoryPort
from jb.shared_kernel.value_objects import UserId

# 데모 고객 식별자 — 프론트엔드와 공유한다.
GENERAL_USER_ID = "user_kim_sonja"
CORPORATE_USER_ID = "user_park_corp"

_DEFAULT = CustomerProfile(name="김순자", age=72)

# 일반 창구 고객(김순자)과 법인 사무창구 고객(박상호 대표)을 user_id로 구별한다.
_CUSTOMERS: dict[str, CustomerProfile] = {
    GENERAL_USER_ID: _DEFAULT,
    CORPORATE_USER_ID: CustomerProfile(name="박상호", age=48),
}


class MockCustomerDirectory(CustomerDirectoryPort):
    """
    해커톤 데모용 Mock 구현. user_id로 일반 고객(김순자)과 법인 사무 고객(박상호)을 돌려준다.
    알 수 없는 id는 기본 고객(김순자)으로 폴백한다.
    실 서비스 전환 시 CustomerDbDirectory로 교체 — 유스케이스 코드 변경 0 (DIP).
    """

    async def get(self, user_id: UserId) -> CustomerProfile:
        return _CUSTOMERS.get(user_id.value, _DEFAULT)
