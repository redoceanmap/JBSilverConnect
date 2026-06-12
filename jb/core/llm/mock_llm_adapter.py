from __future__ import annotations

from jb.core.ports.llm_port import LlmPort


class MockLlmAdapter(LlmPort):
    """
    키 없는 데모용 최종 폴백. 항상 성공한다.
    LSP: 동일 계약을 지키므로 폴백 체인 마지막에서 무손실 치환된다.
    """

    async def generate(self, prompt: str) -> str:
        return "고객님, 준비된 안내를 알려드릴게요. (데모 응답)"
