from __future__ import annotations

import enum
from dataclasses import dataclass


class WindowType(enum.Enum):
    """창구 종류. 멤버가 번호표 접두를 들고 직접 번호를 포맷한다(타입 분기 회피).

    GENERAL(일반): 접두 없음. CORPORATE(법인 사무): 'B' 접두로 법인 창구에서 구별 호출.
    """

    GENERAL = ("general", "")
    CORPORATE = ("corporate", "B")

    def __init__(self, code: str, ticket_prefix: str) -> None:
        self.code = code
        self.ticket_prefix = ticket_prefix

    def format_ticket(self, number: int) -> str:
        """대기번호에 창구 접두를 붙인다. 예: 법인 3번 → 'B3'."""
        return f"{self.ticket_prefix}{number}"


def window_type_from_code(code: str) -> WindowType:
    """창구 종류 코드 문자열을 WindowType으로 해석한다. 미일치 시 일반 창구로 본다."""
    for window_type in WindowType:
        if window_type.code == code:
            return window_type
    return WindowType.GENERAL


@dataclass(frozen=True)
class Money:
    """금액 값 객체. 음수 불가, 원 단위. 불변."""

    amount: int

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("금액은 음수일 수 없습니다")

    def is_idle_over(self, threshold: "Money") -> bool:
        """유휴 잔액이 기준선 이상인지 — 분기 대신 도메인 의도를 드러내는 행위."""
        return self.amount >= threshold.amount


@dataclass(frozen=True)
class UserId:
    """사용자 식별자 값 객체. 빈 값 불가. 불변."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("UserId는 비어 있을 수 없습니다")
