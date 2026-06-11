from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.phishing.app.dtos.phishing_dto import CheckPhishingCommand, PhishingView


class CheckPhishingUseCase(ABC):
    """Driving Port — 피싱 신호등 판정 유스케이스 계약."""

    @abstractmethod
    async def execute(self, command: CheckPhishingCommand) -> PhishingView: ...
