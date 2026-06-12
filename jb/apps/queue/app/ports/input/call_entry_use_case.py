from __future__ import annotations

from abc import ABC, abstractmethod


class CallEntryUseCase(ABC):
    """Driving Port — 현장대기 고객을 호출하는 계약."""

    @abstractmethod
    async def execute(self, handoff_id: str) -> None: ...
