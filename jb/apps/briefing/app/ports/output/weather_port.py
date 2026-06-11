from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.briefing.domain.value_objects.briefing_vo import Weather


class WeatherPort(ABC):
    """날씨 조회 추상화. 구현은 Adapter(Mock / 기상청 API)가 담당."""

    @abstractmethod
    async def today(self) -> Weather: ...
