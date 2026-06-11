from __future__ import annotations

from jb.apps.branch.app.ports.output.map_port import MapPort
from jb.apps.branch.domain.entities.branch_entity import Branch
from jb.apps.branch.domain.value_objects.branch_vo import GeoCoordinate


class FallbackMapAdapter(MapPort):
    """
    데코레이터 패턴 + LSP.
    앞선 어댑터가 실패하면 다음 순위로 폴백한다. 호출부는 단일 MapPort만 알면 된다.
    분기(if-else)가 아니라 순차 시도(loop + 예외 처리)로 OCP·LSP를 만족.
    """

    def __init__(self, adapters: list[MapPort]) -> None:
        if not adapters:
            raise ValueError("최소 1개의 지도 어댑터가 필요합니다")
        self._adapters = adapters

    async def find_nearby(self, origin: GeoCoordinate, limit: int) -> list[Branch]:
        last_error: Exception = RuntimeError("실행된 어댑터가 없습니다")
        for adapter in self._adapters:
            try:
                return await adapter.find_nearby(origin, limit)
            except Exception as error:
                last_error = error
        raise last_error
