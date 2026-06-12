from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """환경 설정 값 객체. 불변. 키 미설정 시 빈 문자열 → 어댑터가 가드로 폴백."""

    gemini_api_key: str
    groq_api_key: str
    naver_client_id: str
    naver_client_secret: str
    demo_user_id: str


def load_settings() -> Settings:
    return Settings(
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        groq_api_key=os.getenv("GROQ_API_KEY", ""),
        naver_client_id=os.getenv("NAVER_CLIENT_ID", ""),
        naver_client_secret=os.getenv("NAVER_CLIENT_SECRET", ""),
        demo_user_id=os.getenv("DEMO_USER_ID", "user_kim_sonja"),
    )


settings = load_settings()
