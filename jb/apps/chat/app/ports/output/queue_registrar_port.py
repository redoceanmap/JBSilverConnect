from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from jb.apps.chat.domain.entities.staff_handoff import StaffHandoff


class QueueRegistrarPort(ABC):
    """창구 대기열 등록 추상화 — Driven Port. 전달된 핸드오프를 대기열에 올린다."""

    @abstractmethod
    async def register(self, handoff: StaffHandoff, created_at: datetime) -> None: ...
