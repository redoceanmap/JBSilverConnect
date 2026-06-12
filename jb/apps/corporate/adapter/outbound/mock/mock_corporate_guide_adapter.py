from __future__ import annotations

from dataclasses import dataclass

from jb.apps.corporate.app.ports.output.corporate_guide_port import CorporateGuidePort
from jb.apps.corporate.domain.value_objects.corporate_vo import (
    CorporateTaskGuide,
    GeoPoint,
    IssuingInstitution,
)


@dataclass(frozen=True)
class _Candidate:
    name: str
    coordinate: GeoPoint


@dataclass(frozen=True)
class _TaskSpec:
    task_name: str
    required_docs: tuple[str, ...]
    estimated_cost: str
    institution_kind: str
    candidates: tuple[_Candidate, ...]


# 업무별 발급 기관 추천 개수(가까운 순).
_RECOMMEND_LIMIT = 3

# 세무서 후보 — 전국 주요 세무서.
_TAX_OFFICES: tuple[_Candidate, ...] = (
    _Candidate("전주세무서", GeoPoint(35.8217, 127.1469)),
    _Candidate("군산세무서", GeoPoint(35.9676, 126.7370)),
    _Candidate("광주세무서", GeoPoint(35.1595, 126.8526)),
    _Candidate("종로세무서", GeoPoint(37.5704, 126.9910)),
    _Candidate("강남세무서", GeoPoint(37.5172, 127.0473)),
)

# 등기소(관할 법원 등기과) 후보.
_REGISTRIES: tuple[_Candidate, ...] = (
    _Candidate("전주지방법원 등기과", GeoPoint(35.8252, 127.1340)),
    _Candidate("광주지방법원 등기과", GeoPoint(35.1510, 126.8870)),
    _Candidate("서울중앙지방법원 등기국", GeoPoint(37.4894, 127.0086)),
    _Candidate("서울북부지방법원 등기국", GeoPoint(37.6396, 127.0257)),
)

# 은행 지점(법인 통장 개설·담보 감정) 후보.
_BANK_BRANCHES: tuple[_Candidate, ...] = (
    _Candidate("전북은행 본점", GeoPoint(35.8242, 127.1480)),
    _Candidate("전북은행 효자동지점", GeoPoint(35.8333, 127.1100)),
    _Candidate("전북은행 서울지점", GeoPoint(37.5663, 126.9779)),
    _Candidate("광주은행 본점", GeoPoint(35.1510, 126.9110)),
)

# 주민센터/구청(주민등록·인감증명) 후보.
_COMMUNITY_CENTERS: tuple[_Candidate, ...] = (
    _Candidate("전주 완산구청", GeoPoint(35.8120, 127.1080)),
    _Candidate("전주 덕진구청", GeoPoint(35.8470, 127.1290)),
    _Candidate("서울 종로구청", GeoPoint(37.5735, 126.9790)),
    _Candidate("서울 강남구청", GeoPoint(37.5172, 127.0473)),
)

# 큐레이션 데모 데이터. 실 서비스 전환 시 정부24·기관 API 어댑터로 교체 — 유스케이스 변경 0.
_CORPORATE_TASKS: tuple[_TaskSpec, ...] = (
    _TaskSpec(
        task_name="사업자등록",
        required_docs=("대표자 신분증", "사업장 임대차계약서", "사업자등록 신청서"),
        estimated_cost="무료",
        institution_kind="세무서",
        candidates=_TAX_OFFICES,
    ),
    _TaskSpec(
        task_name="법인설립등기",
        required_docs=("정관", "주주명부", "잔고증명서", "임원 취임승낙서"),
        estimated_cost="등록면허세·지방교육세 등 약 11만 원~ (자본금에 따라 상이)",
        institution_kind="등기소",
        candidates=_REGISTRIES,
    ),
    _TaskSpec(
        task_name="법인 인감증명서 발급",
        required_docs=("법인 인감카드", "대표자 신분증"),
        estimated_cost="1통 약 1,000원",
        institution_kind="등기소",
        candidates=_REGISTRIES,
    ),
    _TaskSpec(
        task_name="법인 통장(사업자통장) 개설",
        required_docs=("사업자등록증", "법인 인감증명서", "법인 등기부등본", "대표자 신분증"),
        estimated_cost="무료",
        institution_kind="은행 지점",
        candidates=_BANK_BRANCHES,
    ),
)

_MORTGAGE_TASKS: tuple[_TaskSpec, ...] = (
    _TaskSpec(
        task_name="부동산 등기부등본 발급",
        required_docs=("부동산 소재지", "신분증"),
        estimated_cost="1통 약 1,000원 (인터넷등기소 700원)",
        institution_kind="등기소",
        candidates=_REGISTRIES,
    ),
    _TaskSpec(
        task_name="주민등록등본·인감증명서 발급",
        required_docs=("신분증",),
        estimated_cost="통당 약 400~1,200원",
        institution_kind="주민센터",
        candidates=_COMMUNITY_CENTERS,
    ),
    _TaskSpec(
        task_name="소득금액증명원 발급",
        required_docs=("신분증",),
        estimated_cost="무료 (홈택스·세무서)",
        institution_kind="세무서",
        candidates=_TAX_OFFICES,
    ),
    _TaskSpec(
        task_name="담보 부동산 감정평가",
        required_docs=("부동산 등기권리증(등기필증)", "신분증"),
        estimated_cost="감정평가 수수료 별도 (은행 안내)",
        institution_kind="은행 지점",
        candidates=_BANK_BRANCHES,
    ),
)

# 주제별 큐레이션 업무 목록. 알 수 없는 주제는 법인 사무로 폴백한다.
_TASKS_BY_TOPIC: dict[str, tuple[_TaskSpec, ...]] = {
    "corporate": _CORPORATE_TASKS,
    "mortgage": _MORTGAGE_TASKS,
}


class MockCorporateGuideAdapter(CorporateGuidePort):
    """큐레이션 방문 준비 데이터. 주제별로 필요 서류·비용과 가까운 발급 기관을 추천한다."""

    async def guide(self, origin: GeoPoint, topic: str) -> list[CorporateTaskGuide]:
        specs = _TASKS_BY_TOPIC.get(topic, _CORPORATE_TASKS)
        return [self._build(spec, origin) for spec in specs]

    def _build(self, spec: _TaskSpec, origin: GeoPoint) -> CorporateTaskGuide:
        nearest_first = sorted(
            spec.candidates,
            key=lambda candidate: origin.distance_meters_to(candidate.coordinate),
        )
        institutions = tuple(
            IssuingInstitution(
                name=candidate.name,
                kind=spec.institution_kind,
                distance_meters=origin.distance_meters_to(candidate.coordinate),
            )
            for candidate in nearest_first[:_RECOMMEND_LIMIT]
        )
        return CorporateTaskGuide(
            task_name=spec.task_name,
            required_docs=spec.required_docs,
            estimated_cost=spec.estimated_cost,
            institutions=institutions,
        )
