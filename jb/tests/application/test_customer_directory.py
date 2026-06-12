from __future__ import annotations

import pytest

from jb.core.customer.mock_customer_directory import (
    CORPORATE_USER_ID,
    GENERAL_USER_ID,
    MockCustomerDirectory,
)
from jb.shared_kernel.value_objects import UserId


@pytest.mark.asyncio
async def test_일반_고객은_김순자다():
    directory = MockCustomerDirectory()
    customer = await directory.get(UserId(GENERAL_USER_ID))
    assert customer.name == "김순자"
    assert customer.age == 72


@pytest.mark.asyncio
async def test_법인_사무_고객은_박상호다():
    directory = MockCustomerDirectory()
    customer = await directory.get(UserId(CORPORATE_USER_ID))
    assert customer.name == "박상호"


@pytest.mark.asyncio
async def test_알_수_없는_id는_기본_고객으로_폴백한다():
    directory = MockCustomerDirectory()
    customer = await directory.get(UserId("unknown"))
    assert customer.name == "김순자"
