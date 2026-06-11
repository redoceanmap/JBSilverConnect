from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CustomerProfile:
    """창구 직원에게 보여줄 고객 신상 값 객체. 불변."""

    name: str
    age: int

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("고객 이름은 비어 있을 수 없습니다")
        if self.age < 0:
            raise ValueError("나이는 음수일 수 없습니다")

    def label(self) -> str:
        """표시용 '이름 (나이)' 라벨."""
        return f"{self.name} ({self.age})"
