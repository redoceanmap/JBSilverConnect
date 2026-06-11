from __future__ import annotations

from jb.apps.phishing.app.ports.output.llm_port import PhishingLlmPort

_DANGER_KEYWORDS = ("안전계좌", "송금", "이체", "검찰", "구속", "벌금", "보안카드")
_WARNING_KEYWORDS = ("계좌", "비밀번호", "인증번호", "카드번호", "대출")


class MockPhishingLlmAdapter(PhishingLlmPort):
    """
    데모용 룰베이스 스텁. 네트워크/키 없이 메시지의 위험 키워드로 'safe'·'warning'·'danger'를 판정한다.
    실 서비스 전환 시 ClaudePhishingLlmAdapter로 교체 — 유스케이스 변경 0 (LSP).
    """

    async def generate(self, prompt: str) -> str:
        if any(keyword in prompt for keyword in _DANGER_KEYWORDS):
            return "danger"
        if any(keyword in prompt for keyword in _WARNING_KEYWORDS):
            return "warning"
        return "safe"
