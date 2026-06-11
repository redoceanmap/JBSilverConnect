from __future__ import annotations

from jb.apps.briefing.app.ports.output.tts_port import TtsPort


class MockTtsAdapter(TtsPort):
    """
    데모용 음성 합성. 네트워크 없이 텍스트를 바이트로 인코딩만 한다.
    실 서비스 전환 시 GttsAdapter로 교체 — 유스케이스 변경 0 (LSP).
    """

    async def synthesize(self, text: str) -> bytes:
        return text.encode("utf-8")
