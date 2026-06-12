from __future__ import annotations

from abc import ABC, abstractmethod


class ConfirmArrivalUseCase(ABC):
    """Driving Port — 대기 고객의 현장 도착을 인증하는 계약."""

    @abstractmethod
    async def execute(self, handoff_id: str) -> None: ...
