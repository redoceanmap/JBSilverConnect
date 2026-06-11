from __future__ import annotations

from abc import ABC, abstractmethod


class TtsPort(ABC):
    """음성 합성 추상화. ISP: '텍스트 → 오디오 바이트' 책임만 가진다."""

    @abstractmethod
    async def synthesize(self, text: str) -> bytes: ...
