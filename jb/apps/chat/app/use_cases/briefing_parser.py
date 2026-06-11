from __future__ import annotations

import json

from jb.apps.chat.domain.value_objects.handoff_vo import VisitBriefing

_FALLBACK = VisitBriefing(
    purpose="상담 요청",
    target="—",
    amount="—",
    required_docs="신분증",
    special_notes="천천히 설명이 필요한 고객입니다.",
    advice="고객 말씀을 천천히 확인하며 도와드리면 좋아요.",
)


def _strip_code_fence(raw: str) -> str:
    """LLM이 감싸 보내는 ```json … ``` 펜스를 벗긴다."""
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[len("json"):]
    return text.strip().strip("`").strip()


def parse_briefing(raw: str) -> VisitBriefing:
    """LLM JSON 응답을 VisitBriefing으로 파싱한다. 형식이 깨지면 안전한 기본값으로 폴백."""
    try:
        data = json.loads(_strip_code_fence(raw))
    except (json.JSONDecodeError, ValueError):
        return _FALLBACK
    if not isinstance(data, dict):
        return _FALLBACK
    return VisitBriefing(
        purpose=str(data.get("purpose") or _FALLBACK.purpose),
        target=str(data.get("target") or _FALLBACK.target),
        amount=str(data.get("amount") or _FALLBACK.amount),
        required_docs=str(data.get("required_docs") or _FALLBACK.required_docs),
        special_notes=str(data.get("special_notes") or _FALLBACK.special_notes),
        advice=str(data.get("advice") or _FALLBACK.advice),
    )
