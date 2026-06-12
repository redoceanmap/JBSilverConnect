from __future__ import annotations

from jb.apps.branch.app.ports.output.map_port import MapPort
from jb.apps.branch.domain.entities.branch_entity import Branch
from jb.apps.branch.domain.value_objects.branch_vo import (
    Distance,
    GeoCoordinate,
    WaitStatus,
)


class MockMapAdapter(MapPort):
    """데모용 지점 데이터. 실 서비스 전환 시 NaverMapAdapter로 교체 — 유스케이스 변경 0."""

    async def find_nearby(self, origin: GeoCoordinate, limit: int) -> list[Branch]:
        branches = [
            Branch("전북은행 본점", GeoCoordinate(35.8242, 127.1480), Distance(320), WaitStatus(2)),
            Branch("전북은행 효자동지점", GeoCoordinate(35.8333, 127.1100), Distance(880), WaitStatus(5)),
            Branch("전북은행 서신동지점", GeoCoordinate(35.8290, 127.1200), Distance(1500), WaitStatus(0)),
        ]
        return branches[:limit]
