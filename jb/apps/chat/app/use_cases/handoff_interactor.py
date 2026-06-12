from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from jb.apps.chat.app.dtos.chat_dto import HandoffCommand, StaffHandoffView
from jb.apps.chat.app.ports.input.handoff_use_case import HandoffUseCase
from jb.apps.chat.app.ports.output.handoff_store_port import HandoffStorePort
from jb.apps.chat.app.ports.output.queue_registrar_port import QueueRegistrarPort
from jb.apps.chat.app.use_cases.briefing_parser import parse_briefing
from jb.apps.chat.app.use_cases.conversation_assembler import assemble_conversation
from jb.apps.chat.app.use_cases.handoff_view_mapper import to_card
from jb.apps.chat.domain.entities.staff_handoff import StaffHandoff
from jb.core.ports.customer_directory_port import CustomerDirectoryPort
from jb.core.ports.llm_port import LlmPort
from jb.shared_kernel.value_objects import UserId

_HANDOFF_INSTRUCTION = (
    "다음은 노년층 고객과 JB 도우미가 나눈 대화다. "
    "은행 창구 직원이 한눈에 파악하도록 아래 JSON 형식으로만 정리해라. "
    "JSON 외의 다른 말이나 코드펜스 설명은 출력하지 마라.\n"
    "{\n"
    '  "purpose": "방문 목적 (예: 현금 입금 + 통장 정리)",\n'
    '  "target": "관련 계좌/상품 (예: 전북은행 입출금통장)",\n'
    '  "amount": "관련 금액 (예: 현금 약 5만 원, 없으면 \'해당 없음\')",\n'
    '  "required_docs": "필요 서류 (예: 통장·신분증)",\n'
    '  "special_notes": "특이사항 (예: 천천히 설명 필요)",\n'
    '  "advice": "직원이 미리 준비하면 좋을 점을 정중한 한 문장으로"\n'
    "}\n\n"
    "[대화]\n"
)

_CONFIRM_MESSAGE = "가까운 지점 직원에게 내용을 전달했어요. 곧 도와드릴 거예요. 😊"


class HandoffInteractor(HandoffUseCase):
    """SRP: 대화를 구조화한 뒤 창구 전달함에 보관하고, 전달 카드를 돌려주는 것만 책임진다."""

    def __init__(
        self,
        llm: LlmPort,
        store: HandoffStorePort,
        directory: CustomerDirectoryPort,
        registrar: QueueRegistrarPort,
    ) -> None:
        self._llm = llm
        self._store = store
        self._directory = directory
        self._registrar = registrar

    async def execute(self, command: HandoffCommand) -> StaffHandoffView:
        conversation = assemble_conversation(command.history)
        prompt = f"{_HANDOFF_INSTRUCTION}{conversation.transcript()}"
        briefing = parse_briefing(await self._llm.generate(prompt))
        customer = await self._directory.get(UserId(command.user_id))

        handoff = StaffHandoff(
            handoff_id=uuid4().hex,
            customer=customer,
            briefing=briefing,
            original_message=_original_message(command),
        )
        await self._store.save(handoff)
        await self._registrar.register(handoff, datetime.now(timezone.utc))

        queue = await self._store.list_active()
        return StaffHandoffView(
            card=to_card(handoff, queue_position=len(queue) - 1),
            confirm_message=_CONFIRM_MESSAGE,
        )


def _original_message(command: HandoffCommand) -> str:
    """직원에게 그대로 보여줄 고객 원문 — 사용자 발화만 이어 붙인다."""
    spoken = [item.text.strip() for item in command.history if item.role == "user"]
    return " ".join(text for text in spoken if text)
