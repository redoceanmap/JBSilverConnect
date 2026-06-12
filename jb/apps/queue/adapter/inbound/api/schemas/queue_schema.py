from __future__ import annotations

from pydantic import BaseModel


class QueueEntryCardResponse(BaseModel):
    handoff_id: str
    customer_name: str
    customer_age: int
    ticket_number: int
    ticket_label: str
    window_type: str
    eta_text: str
    purpose: str
    target: str
    amount: str
    required_docs: str
    special_notes: str
    advice: str
    original_message: str
    status: str
    remaining_seconds: int
