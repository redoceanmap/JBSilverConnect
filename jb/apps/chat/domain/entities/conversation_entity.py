from __future__ import annotations

from dataclasses import dataclass

from jb.apps.chat.domain.value_objects.chat_vo import Utterance


@dataclass(frozen=True)
class Conversation:
    """어르신과 도우미가 주고받은 대화 전체."""

    utterances: tuple[Utterance, ...]

    def __post_init__(self) -> None:
        if not self.utterances:
            raise ValueError("대화에는 최소 한 마디가 필요합니다")

    def transcript(self) -> str:
        """LLM 프롬프트에 넣을 대화록 문자열로 펼친다."""
        return "\n".join(utterance.render() for utterance in self.utterances)
