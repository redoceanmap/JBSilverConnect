from __future__ import annotations

from abc import ABC, abstractmethod


class PhishingLlmPort(ABC):
    """Driven Port — 피싱 판정용 LLM 추상화. ISP: '텍스트 생성' 책임만 가진다."""

    @abstractmethod
    async def generate(self, prompt: str) -> str: ...
