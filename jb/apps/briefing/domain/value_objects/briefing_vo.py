from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Weather:
    """오늘 날씨 값 객체. 불변."""

    temperature: int
    description: str

    def __post_init__(self) -> None:
        if not self.description:
            raise ValueError("날씨 설명은 비어 있을 수 없습니다")


@dataclass(frozen=True)
class BriefingContent:
    """브리핑 음성 안내 문구 값 객체. 불변."""

    text: str

    def __post_init__(self) -> None:
        if not self.text:
            raise ValueError("브리핑 내용은 비어 있을 수 없습니다")
