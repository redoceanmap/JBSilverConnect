from __future__ import annotations

import pytest

from jb.apps.savings.domain.entities.savings_proposal_entity import SavingsProposal
from jb.apps.savings.domain.value_objects.savings_vo import InterestRate
from jb.shared_kernel.value_objects import Money, UserId


def _proposal() -> SavingsProposal:
    return SavingsProposal(UserId("u1"), Money(50_000), InterestRate(0.035))


def test_확증형_동의_없이는_이벤트가_없다():
    assert _proposal().pull_events() == []


def test_동의하면_이동_이벤트가_발생한다():
    proposal = _proposal()
    proposal.accept()
    events = proposal.pull_events()
    assert len(events) == 1


def test_월_이자는_잔액_곱하기_연이율_나누기_12():
    assert _proposal().expected_monthly_interest() == Money(145)  # 50000 * 0.035 / 12


def test_이미_동의한_제안은_재동의할_수_없다():
    proposal = _proposal()
    proposal.accept()
    with pytest.raises(ValueError):
        proposal.accept()
