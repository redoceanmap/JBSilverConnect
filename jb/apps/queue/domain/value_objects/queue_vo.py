from __future__ import annotations

import enum


class QueueStatus(enum.Enum):
    """창구 대기열 고객 상태.

    WAITING(대기): 번호표 발급 후 아직 현장 미도착.
    ON_SITE(현장대기): 직원이 도착 인증을 누른 상태.
    CALLED(호출): 직원이 호출한 상태. 잠시 뒤 자동 삭제된다.
    """

    WAITING = "waiting"
    ON_SITE = "on_site"
    CALLED = "called"
