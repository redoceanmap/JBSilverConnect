from __future__ import annotations

from jb.apps.phishing.app.ports.output.llm_port import PhishingLlmPort


class MockPhishingLlmAdapter(PhishingLlmPort):
    """
    데모용 LLM 스텁. 네트워크 없이 항상 'safe'를 반환한다.
    실 서비스 전환 시 ClaudePhishingLlmAdapter로 교체 — 유스케이스 변경 0 (LSP).
    """

    async def generate(self, prompt: str) -> str:
        pass
