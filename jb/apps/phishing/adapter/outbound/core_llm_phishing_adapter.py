from __future__ import annotations

from jb.apps.phishing.app.ports.output.llm_port import PhishingLlmPort
from jb.core.ports.llm_port import LlmPort


class CoreLlmPhishingAdapter(PhishingLlmPort):
    """공용 core LLM(Gemini→Mock 폴백)을 피싱 전용 포트로 잇는 어댑터.
    LSP: 동일 계약(prompt in → text out)이라 무손실 위임."""

    def __init__(self, llm: LlmPort) -> None:
        self._llm = llm

    async def generate(self, prompt: str) -> str:
        return await self._llm.generate(prompt)
