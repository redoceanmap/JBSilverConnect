from __future__ import annotations

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field("user", description="발화 주체: 'user' 또는 'assistant'")
    text: str = Field(..., description="발화 내용")


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(..., description="지금까지의 대화(최신 사용자 발화 포함)")


class HandoffRequest(ChatRequest):
    user_id: str = Field("user_kim_sonja", description="어르신 사용자 ID")


class ChatReplyResponse(BaseModel):
    reply: str


class HandoffCardResponse(BaseModel):
    handoff_id: str
    customer_name: str
    customer_age: int
    ticket_number: int
    eta_text: str
    purpose: str
    target: str
    amount: str
    required_docs: str
    special_notes: str
    advice: str
    original_message: str


class HandoffResponse(BaseModel):
    card: HandoffCardResponse
    confirm_message: str
