from __future__ import annotations

from jb.core.ports.llm_port import LlmPort


class FallbackLlmAdapter(LlmPort):
    """
    데코레이터 패턴 + LSP.
    앞선 어댑터가 실패하면 다음 순위로 폴백한다. 호출부는 단일 LlmPort만 알면 된다.
    분기(if-else)가 아니라 순차 시도(loop + 예외 처리)로 OCP·LSP를 만족.
    """

    def __init__(self, adapters: list[LlmPort]) -> None:
        if not adapters:
            raise ValueError("최소 1개의 LLM 어댑터가 필요합니다")
        self._adapters = adapters

    async def generate(self, prompt: str) -> str:
        last_error: Exception = RuntimeError("실행된 어댑터가 없습니다")
        for adapter in self._adapters:
            try:
                return await adapter.generate(prompt)
            except Exception as error:
                last_error = error
        raise last_error
