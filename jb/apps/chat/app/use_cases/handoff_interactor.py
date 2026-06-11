from __future__ import annotations

from jb.apps.chat.app.dtos.chat_dto import HandoffCommand, StaffHandoffView
from jb.apps.chat.app.ports.input.handoff_use_case import HandoffUseCase
from jb.apps.chat.app.use_cases.conversation_assembler import assemble_conversation
from jb.core.ports.llm_port import LlmPort

_HANDOFF_INSTRUCTION = (
    "다음은 노년층 고객과 JB 도우미가 나눈 대화다. "
    "이 대화를 은행 창구 직원이 한눈에 파악하도록 요약해라. "
    "고객이 원하는 것(핵심 용건), 관련 정보, 직원이 준비하면 좋을 점을 "
    "정중한 문장으로 3~4줄로 정리한다. 인사말이나 사족 없이 요약만 출력한다.\n\n"
    "[대화]\n"
)

_CONFIRM_MESSAGE = "가까운 지점 직원에게 내용을 전달했어요. 곧 도와드릴 거예요. 😊"


class HandoffInteractor(HandoffUseCase):
    """SRP: 대화를 직원 전달용 요약으로 만드는 것만 책임진다."""

    def __init__(self, llm: LlmPort) -> None:
        self._llm = llm

    async def execute(self, command: HandoffCommand) -> StaffHandoffView:
        conversation = assemble_conversation(command.history)
        prompt = f"{_HANDOFF_INSTRUCTION}{conversation.transcript()}"
        summary = await self._llm.generate(prompt)
        return StaffHandoffView(
            summary=summary.strip(),
            confirm_message=_CONFIRM_MESSAGE,
        )
