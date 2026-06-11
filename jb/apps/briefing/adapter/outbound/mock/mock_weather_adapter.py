from __future__ import annotations

from jb.apps.briefing.app.ports.output.weather_port import WeatherPort
from jb.apps.briefing.domain.value_objects.briefing_vo import Weather


class MockWeatherAdapter(WeatherPort):
    """데모용 날씨. 실 서비스 전환 시 기상청 API 어댑터로 교체 — 유스케이스 변경 0."""

    async def today(self) -> Weather:
        return Weather(temperature=23, description="맑음")
