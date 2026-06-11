from __future__ import annotations

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field("user", description="발화 주체: 'user' 또는 'assistant'")
    text: str = Field(..., description="발화 내용")


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(..., description="지금까지의 대화(최신 사용자 발화 포함)")


class ChatReplyResponse(BaseModel):
    reply: str


class HandoffResponse(BaseModel):
    summary: str
    confirm_message: str
