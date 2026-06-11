from __future__ import annotations

from jb.apps.chat.app.ports.input.converse_use_case import ConverseUseCase
from jb.apps.chat.app.ports.input.handoff_use_case import HandoffUseCase
from jb.apps.chat.app.use_cases.converse_interactor import ConverseInteractor
from jb.apps.chat.app.use_cases.handoff_interactor import HandoffInteractor
from jb.core.di import get_llm


def get_converse_use_case() -> ConverseUseCase:
    return ConverseInteractor(llm=get_llm())


def get_handoff_use_case() -> HandoffUseCase:
    return HandoffInteractor(llm=get_llm())
