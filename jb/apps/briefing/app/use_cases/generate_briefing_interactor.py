from __future__ import annotations

from jb.apps.briefing.app.dtos.briefing_dto import BriefingView, GenerateBriefingCommand
from jb.apps.briefing.app.ports.input.generate_briefing_use_case import (
    GenerateBriefingUseCase,
)
from jb.apps.briefing.app.ports.output.tts_port import TtsPort
from jb.apps.briefing.app.ports.output.weather_port import WeatherPort
from jb.apps.briefing.domain.entities.daily_briefing_entity import DailyBriefing
from jb.apps.briefing.domain.value_objects.briefing_vo import BriefingContent
from jb.core.ports.account_query_port import AccountQueryPort
from jb.core.ports.llm_port import LlmPort
from jb.shared_kernel.value_objects import UserId


class GenerateBriefingInteractor(GenerateBriefingUseCase):
    """
    SRP: '아침 브리핑 생성'만 책임진다.
    DIP: 계좌·날씨·LLM·TTS Port에만 의존(구체 구현 모름).
    """

    def __init__(
        self,
        account_query: AccountQueryPort,
        weather: WeatherPort,
        llm: LlmPort,
        tts: TtsPort,
    ) -> None:
        self._account_query = account_query
        self._weather = weather
        self._llm = llm
        self._tts = tts

    async def execute(self, command: GenerateBriefingCommand) -> BriefingView:
        user_id = UserId(command.user_id)
        balance = await self._account_query.get_balance(user_id)
        weather = await self._weather.today()

        text = await self._llm.generate(
            f"어르신께 오늘 잔액 {balance.amount}원, 날씨는 {weather.description}"
            f"({weather.temperature}도)라고 따뜻하게 아침 인사해줘"
        )
        briefing = DailyBriefing(
            balance=balance,
            weather=weather,
            content=BriefingContent(text),
        )
        spoken = briefing.spoken_text()
        audio = await self._tts.synthesize(spoken)

        return BriefingView(
            balance=balance.amount,
            weather_description=weather.description,
            temperature=weather.temperature,
            spoken_text=spoken,
            audio_size_bytes=len(audio),
        )
