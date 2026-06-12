from __future__ import annotations

from jb.apps.chat.app.dtos.chat_dto import ChatReplyView, ConverseCommand
from jb.apps.chat.app.ports.input.converse_use_case import ConverseUseCase
from jb.apps.chat.app.use_cases.conversation_assembler import assemble_conversation
from jb.core.ports.llm_port import LlmPort

_PERSONA = (
    "너는 전북·광주은행(JB금융그룹)의 금융 도우미 'JB AI Connect'다. "
    "모든 고객에게 친근한 존댓말로, 한 번에 한 가지씩 쉽고 명확하게 안내한다. "
    "어려운 금융 용어는 풀어서 설명한다. "
    "가까운 지점 찾기, 은행 방문 예약(번호표), 법인 사무 안내(창업·사업자등록·법인 통장 발급), "
    "부동산 담보대출 필요 서류 안내(필요 서류·예상 비용·가까운 발급 기관)를 도울 수 있다. "
    "법인 업무나 부동산 담보대출로 보이면 '필요 서류 안내를 받아보시겠어요?'라고 제안한다. "
    "답변은 3문장 이내로 한다."
)


class ConverseInteractor(ConverseUseCase):
    """SRP: 고객님의 말에 도우미 한 마디로 응답하는 것만 책임진다.
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
