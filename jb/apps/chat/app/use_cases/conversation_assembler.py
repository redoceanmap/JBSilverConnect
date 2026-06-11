from __future__ import annotations

from collections.abc import Sequence

from jb.apps.chat.app.dtos.chat_dto import UtteranceInput
from jb.apps.chat.domain.entities.conversation_entity import Conversation
from jb.apps.chat.domain.value_objects.chat_vo import Utterance

# role → 화자 라벨. 타입 분기(if-else) 대신 dict 디스패치로 매핑한다.
_SPEAKER_LABELS = {"user": "사용자", "assistant": "도우미"}
_DEFAULT_SPEAKER = "사용자"


def assemble_conversation(history: Sequence[UtteranceInput]) -> Conversation:
    """입력 발화 목록을 도메인 Conversation으로 조립한다."""
    utterances = tuple(
        Utterance(
            speaker=_SPEAKER_LABELS.get(item.role, _DEFAULT_SPEAKER),
            text=item.text,
        )
        for item in history
        if item.text.strip()
    )
    return Conversation(utterances=utterances)
