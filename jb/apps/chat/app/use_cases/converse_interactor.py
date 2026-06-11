from __future__ import annotations

from jb.apps.chat.app.dtos.chat_dto import ChatReplyView, ConverseCommand
from jb.apps.chat.app.ports.input.converse_use_case import ConverseUseCase
from jb.apps.chat.app.use_cases.conversation_assembler import assemble_conversation
from jb.core.ports.llm_port import LlmPort

_PERSONA = (
    "너는 전북·광주은행(JB금융그룹)의 노년층 전용 금융 도우미 'JB 도우미'다. "
    "어르신이 편하게 느끼도록 짧고 친근한 존댓말로, 한 번에 한 가지만 쉽게 안내한다. "
    "사투리로 물어봐도 자연스럽게 알아듣고 답한다. 어려운 금융 용어는 풀어서 설명한다. "
    "적금 제안, 보이스피싱 점검, 잔액·날씨 브리핑, 가까운 지점 찾기, 번호표 예약, 이자 리포트를 도울 수 있다. "
    "필요하면 '제가 가까운 지점 직원에게 전달해 드릴까요?'라고 제안한다. 답변은 3문장 이내로 한다."
)


class ConverseInteractor(ConverseUseCase):
    """SRP: 어르신의 말에 도우미 한 마디로 응답하는 것만 책임진다.
    DIP: 구체 LLM이 아닌 LlmPort에만 의존(키 있으면 Gemini, 없으면 Mock 폴백)."""

    def __init__(self, llm: LlmPort) -> None:
        self._llm = llm

    async def execute(self, command: ConverseCommand) -> ChatReplyView:
        conversation = assemble_conversation(command.history)
        prompt = (
            f"{_PERSONA}\n\n"
            f"[지금까지 대화]\n{conversation.transcript()}\n\n"
            f"도우미:"
        )
        reply = await self._llm.generate(prompt)
        return ChatReplyView(reply=reply.strip())
