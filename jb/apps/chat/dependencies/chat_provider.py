from __future__ import annotations

from functools import lru_cache

from jb.apps.chat.adapter.outbound.mock.in_memory_handoff_store import (
    InMemoryHandoffStore,
)
from jb.apps.chat.app.ports.input.converse_use_case import ConverseUseCase
from jb.apps.chat.app.ports.input.handoff_use_case import HandoffUseCase
from jb.apps.chat.app.ports.input.list_handoffs_use_case import ListHandoffsUseCase
from jb.apps.chat.app.ports.output.handoff_store_port import HandoffStorePort
from jb.apps.chat.app.use_cases.converse_interactor import ConverseInteractor
from jb.apps.chat.app.use_cases.handoff_interactor import HandoffInteractor
from jb.apps.chat.app.use_cases.list_handoffs_interactor import ListHandoffsInteractor
from jb.core.di import get_customer_directory, get_llm


@lru_cache
def _get_handoff_store() -> HandoffStorePort:
    return InMemoryHandoffStore()


def get_converse_use_case() -> ConverseUseCase:
    return ConverseInteractor(llm=get_llm())


def get_handoff_use_case() -> HandoffUseCase:
    return HandoffInteractor(
        llm=get_llm(),
        store=_get_handoff_store(),
        directory=get_customer_directory(),
    )


def get_list_handoffs_use_case() -> ListHandoffsUseCase:
    return ListHandoffsInteractor(store=_get_handoff_store())
