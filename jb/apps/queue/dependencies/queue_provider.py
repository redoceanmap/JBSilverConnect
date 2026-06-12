from __future__ import annotations

from functools import lru_cache

from jb.apps.queue.adapter.outbound.mock.in_memory_queue_repository import (
    InMemoryQueueRepository,
)
from jb.apps.queue.app.ports.input.call_entry_use_case import CallEntryUseCase
from jb.apps.queue.app.ports.input.confirm_arrival_use_case import ConfirmArrivalUseCase
from jb.apps.queue.app.ports.input.list_queue_entries_use_case import (
    ListQueueEntriesUseCase,
)
from jb.apps.queue.app.ports.input.register_queue_entry_use_case import (
    RegisterQueueEntryUseCase,
)
from jb.apps.queue.app.ports.input.remove_queue_entry_use_case import (
    RemoveQueueEntryUseCase,
)
from jb.apps.queue.app.ports.output.queue_entry_repository_port import (
    QueueEntryRepositoryPort,
)
from jb.apps.queue.app.use_cases.call_entry_interactor import CallEntryInteractor
from jb.apps.queue.app.use_cases.confirm_arrival_interactor import (
    ConfirmArrivalInteractor,
)
from jb.apps.queue.app.use_cases.list_queue_entries_interactor import (
    ListQueueEntriesInteractor,
)
from jb.apps.queue.app.use_cases.register_queue_entry_interactor import (
    RegisterQueueEntryInteractor,
)
from jb.apps.queue.app.use_cases.remove_queue_entry_interactor import (
    RemoveQueueEntryInteractor,
)


@lru_cache
def _get_queue_repository() -> QueueEntryRepositoryPort:
    return InMemoryQueueRepository()


def get_register_queue_entry_use_case() -> RegisterQueueEntryUseCase:
    return RegisterQueueEntryInteractor(repository=_get_queue_repository())


def get_remove_queue_entry_use_case() -> RemoveQueueEntryUseCase:
    return RemoveQueueEntryInteractor(repository=_get_queue_repository())


def get_confirm_arrival_use_case() -> ConfirmArrivalUseCase:
    return ConfirmArrivalInteractor(repository=_get_queue_repository())


def get_call_entry_use_case() -> CallEntryUseCase:
    return CallEntryInteractor(repository=_get_queue_repository())


def get_list_queue_entries_use_case() -> ListQueueEntriesUseCase:
    return ListQueueEntriesInteractor(repository=_get_queue_repository())
