from __future__ import annotations

import json

from jb.apps.chat.domain.value_objects.handoff_vo import VisitBriefing

_FALLBACK = VisitBriefing(
    purpose="상담 요청",
    target="—",
    amount="—",
    required_docs="신분증",
    special_notes="—",
    advice="고객 말씀을 확인하며 도와드리면 좋아요.",
    window_type="general",
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
        window_type=_normalize_window_type(data.get("window_type")),
    )


def _normalize_window_type(raw: object) -> str:
    """LLM이 분류한 창구 종류를 정규화한다. 'corporate'만 법인, 그 외/누락은 일반."""
    return "corporate" if str(raw or "").strip().lower() == "corporate" else "general"
