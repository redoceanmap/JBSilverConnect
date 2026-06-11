from __future__ import annotations

from dataclasses import dataclass, field

from jb.apps.savings.domain.events.savings_events import SavingsProposalAccepted
from jb.apps.savings.domain.value_objects.savings_vo import InterestRate
from jb.shared_kernel.domain_event import DomainEvent
from jb.shared_kernel.value_objects import Money, UserId


@dataclass
class SavingsProposal:
    """
    디딤돌 저축 제안 — Aggregate Root.
    확증형 동의 규칙: 반드시 accept()를 거쳐야 이동 이벤트가 발생한다.
    동의 없이는 1원도 움직이지 않는다.
    """

    user_id: UserId
    idle_amount: Money
    rate: InterestRate
    _accepted: bool = field(default=False, init=False)
    _events: list[DomainEvent] = field(default_factory=list, init=False)

    def expected_monthly_interest(self) -> Money:
        return self.rate.monthly_interest_of(self.idle_amount)

    def accept(self) -> None:
        """어르신이 명시적으로 동의한 경우에만 호출. 1원도 동의 없이 안 움직임."""
        if self._accepted:
            raise ValueError("이미 동의 처리된 제안입니다")
        self._accepted = True
        self._events.append(
            SavingsProposalAccepted(user_id=self.user_id, amount=self.idle_amount)
        )

    def is_accepted(self) -> bool:
        return self._accepted

    def pull_events(self) -> list[DomainEvent]:
        events = self._events
        self._events = []
        return events
