from __future__ import annotations

from jb.core.ports.llm_port import LlmPort


class GroqAdapter(LlmPort):
    """LSP: GeminiAdapter와 동일 계약(prompt in → text out). 폴백 시 무손실 교체."""

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    async def generate(self, prompt: str) -> str:
        if not self._api_key:
            raise RuntimeError("GROQ_API_KEY가 설정되지 않았습니다")

        from groq import Groq  # 지연 임포트

        client = Groq(api_key=self._api_key)
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return chat.choices[0].message.content
