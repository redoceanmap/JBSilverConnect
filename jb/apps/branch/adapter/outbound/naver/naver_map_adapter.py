from __future__ import annotations

import math

from jb.apps.branch.app.ports.output.map_port import MapPort
from jb.apps.branch.domain.entities.branch_entity import Branch
from jb.apps.branch.domain.value_objects.branch_vo import Distance, GeoCoordinate, WaitStatus

_SEARCH_URL = "https://openapi.naver.com/v1/search/local.json"
_QUERY = "전북은행"


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> int:
    R = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return round(R * 2 * math.asin(math.sqrt(a)))


class NaverMapAdapter(MapPort):
    """네이버 지역 검색 API로 주변 전북은행 지점을 조회한다.

    거리는 네이버 API가 제공하지 않으므로 Haversine 공식으로 계산한다.
    """

    def __init__(self, client_id: str, client_secret: str) -> None:
        self._client_id = client_id
        self._client_secret = client_secret

    async def find_nearby(self, origin: GeoCoordinate, limit: int) -> list[Branch]:
        if not self._client_id or not self._client_secret:
            raise RuntimeError("NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET가 설정되지 않았습니다")

        import httpx

        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                _SEARCH_URL,
                headers={
                    "X-Naver-Client-Id": self._client_id,
                    "X-Naver-Client-Secret": self._client_secret,
                },
                params={"query": _QUERY, "display": limit, "sort": "random"},
            )
        response.raise_for_status()
        items = response.json()["items"]
        branches = [self._to_branch(item, origin) for item in items]
        branches.sort(key=lambda b: b.distance.meters)
        return branches[:limit]

    def _to_branch(self, item: dict, origin: GeoCoordinate) -> Branch:
        # mapx/mapy는 WGS84 좌표에 1e7을 곱한 정수값
        lat = int(item["mapy"]) / 1e7
        lon = int(item["mapx"]) / 1e7
        name = item["title"].replace("<b>", "").replace("</b>", "")
        distance = _haversine(origin.latitude, origin.longitude, lat, lon)
        return Branch(
            name=name,
            coordinate=GeoCoordinate(latitude=lat, longitude=lon),
            distance=Distance(distance),
            wait_status=WaitStatus(0),
        )
