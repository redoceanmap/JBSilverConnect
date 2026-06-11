from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Utterance:
    """대화 한 마디. speaker는 표시용 화자 라벨('사용자'/'도우미')."""

    speaker: str
    text: str

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("발화 내용이 비어 있습니다")

    def render(self) -> str:
        return f"{self.speaker}: {self.text}"
