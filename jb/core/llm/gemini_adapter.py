from __future__ import annotations

from jb.core.ports.llm_port import LlmPort


class GeminiAdapter(LlmPort):
    """OCP: 새 LLM이 필요하면 이 파일을 수정하지 않고 새 어댑터를 추가한다."""

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    async def generate(self, prompt: str) -> str:
        if not self._api_key:
            raise RuntimeError("GEMINI_API_KEY가 설정되지 않았습니다")

        from google import genai  # 지연 임포트 — 키/패키지 없이도 모듈 로드 가능

        client = genai.Client(api_key=self._api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return response.text
