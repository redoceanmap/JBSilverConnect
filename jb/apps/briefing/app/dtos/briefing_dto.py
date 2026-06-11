from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GenerateBriefingCommand:
    user_id: str


@dataclass(frozen=True)
class BriefingView:
    balance: int
    weather_description: str
    temperature: int
    spoken_text: str
    audio_size_bytes: int
