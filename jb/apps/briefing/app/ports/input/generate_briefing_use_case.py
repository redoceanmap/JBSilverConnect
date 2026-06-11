from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.briefing.app.dtos.briefing_dto import BriefingView, GenerateBriefingCommand


class GenerateBriefingUseCase(ABC):
    """Driving Port — 아침 브리핑 생성 유스케이스 계약."""

    @abstractmethod
    async def execute(self, command: GenerateBriefingCommand) -> BriefingView: ...
