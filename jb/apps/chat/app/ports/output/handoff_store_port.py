from __future__ import annotations

from abc import ABC, abstractmethod

from jb.apps.chat.domain.entities.staff_handoff import StaffHandoff


class HandoffStorePort(ABC):
    """창구 전달 보관 추상화 — Driven Port. 발급 순서를 유지한다."""

    @abstractmethod
    async def save(self, handoff: StaffHandoff) -> None: ...

    @abstractmethod
    async def list_active(self) -> list[StaffHandoff]: ...
