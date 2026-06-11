from __future__ import annotations

from jb.apps.briefing.adapter.outbound.mock.mock_tts_adapter import MockTtsAdapter
from jb.apps.briefing.adapter.outbound.mock.mock_weather_adapter import MockWeatherAdapter
from jb.apps.briefing.app.ports.input.generate_briefing_use_case import (
    GenerateBriefingUseCase,
)
from jb.apps.briefing.app.use_cases.generate_briefing_interactor import (
    GenerateBriefingInteractor,
)
from jb.core.di import get_account_query, get_llm


def get_generate_briefing_use_case() -> GenerateBriefingUseCase:
    return GenerateBriefingInteractor(
        account_query=get_account_query(),
        weather=MockWeatherAdapter(),
        llm=get_llm(),
        tts=MockTtsAdapter(),
    )
