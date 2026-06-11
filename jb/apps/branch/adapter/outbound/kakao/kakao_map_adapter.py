from __future__ import annotations

from jb.apps.branch.app.ports.output.map_port import MapPort
from jb.apps.branch.domain.entities.branch_entity import Branch
from jb.apps.branch.domain.value_objects.branch_vo import (
    Distance,
    GeoCoordinate,
    WaitStatus,
)

_SEARCH_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"
_QUERY = "전북은행"
_RADIUS_METERS = 20000  # 카카오 허용 최대치


class KakaoMapAdapter(MapPort):
    """카카오 로컬 '키워드 장소검색'으로 주변 전북은행 지점을 조회한다.

    거리는 카카오가 제공하는 실측값(미터)을 쓴다.
    창구 대기 인원은 카카오가 제공하지 않으므로 0으로 둔다.
    """

    def __init__(self, rest_key: str) -> None:
        self._rest_key = rest_key

    async def find_nearby(self, origin: GeoCoordinate, limit: int) -> list[Branch]:
        if not self._rest_key:
            raise RuntimeError("KAKAO_REST_KEY가 설정되지 않았습니다")

        import httpx  # 지연 임포트 — 키/패키지 없이도 모듈 로드 가능

        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                _SEARCH_URL,
                headers={"Authorization": f"KakaoAK {self._rest_key}"},
                params={
                    "query": _QUERY,
                    "x": origin.longitude,
                    "y": origin.latitude,
                    "radius": _RADIUS_METERS,
                    "sort": "distance",
                    "size": limit,
                },
            )
        response.raise_for_status()
        documents = response.json()["documents"]
        return [self._to_branch(document) for document in documents]

    def _to_branch(self, document: dict) -> Branch:
        return Branch(
            name=document["place_name"],
            coordinate=GeoCoordinate(
                latitude=float(document["y"]),
                longitude=float(document["x"]),
            ),
            distance=Distance(int(document["distance"])),
            wait_status=WaitStatus(0),
        )
