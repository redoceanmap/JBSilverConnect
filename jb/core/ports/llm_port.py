from __future__ import annotations

from abc import ABC, abstractmethod


class LlmPort(ABC):
    """
    LLM 추상화. ISP에 따라 '텍스트 생성' 책임만 가진다.
    LSP: 모든 구현체는 동일 계약(prompt in → text out)을 지킨다.
    """

    @abstractmethod
    async def generate(self, prompt: str) -> str: ...
