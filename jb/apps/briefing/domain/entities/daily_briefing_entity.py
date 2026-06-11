from __future__ import annotations

from dataclasses import dataclass

from jb.apps.briefing.domain.value_objects.briefing_vo import BriefingContent, Weather
from jb.shared_kernel.value_objects import Money


@dataclass
class DailyBriefing:
    """앱 진입 시 들려줄 아침 브리핑 — Aggregate Root."""

    balance: Money
    weather: Weather
    content: BriefingContent

    def spoken_text(self) -> str:
        return self.content.text
