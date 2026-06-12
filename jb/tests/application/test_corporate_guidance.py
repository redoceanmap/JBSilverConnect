from __future__ import annotations

import pytest

from jb.apps.corporate.adapter.outbound.mock.mock_corporate_guide_adapter import (
    MockCorporateGuideAdapter,
)
from jb.apps.corporate.app.dtos.corporate_dto import CorporateGuideQuery
from jb.apps.corporate.app.use_cases.guide_corporate_affairs_interactor import (
    GuideCorporateAffairsInteractor,
)

# 서울/전주 좌표 — 최근접 기관이 위치에 따라 달라지는지 확인용.
_SEOUL = (37.5665, 126.9780)
_JEONJU = (35.8242, 127.1480)


def _interactor() -> GuideCorporateAffairsInteractor:
    return GuideCorporateAffairsInteractor(guide_provider=MockCorporateGuideAdapter())


@pytest.mark.asyncio
async def test_법인_사무_안내는_서류와_비용과_기관을_포함한다():
    view = await _interactor().execute(
        CorporateGuideQuery(user_id="u1", latitude=_SEOUL[0], longitude=_SEOUL[1])
    )

    assert view.tasks  # 최소 한 건 이상의 업무 안내
    assert any(task.task_name == "사업자등록" for task in view.tasks)
    for task in view.tasks:
        assert task.required_docs  # 필요 서류 비어있지 않음
        assert task.estimated_cost  # 예상 비용 안내됨
        assert task.institutions  # 발급 기관 추천 비어있지 않음
        assert all(inst.distance_meters >= 0 for inst in task.institutions)


@pytest.mark.asyncio
async def test_발급_기관은_가까운_순으로_추천된다():
    view = await _interactor().execute(
        CorporateGuideQuery(user_id="u1", latitude=_SEOUL[0], longitude=_SEOUL[1])
    )
    for task in view.tasks:
        distances = [inst.distance_meters for inst in task.institutions]
        assert distances == sorted(distances)  # 가까운 순 정렬


@pytest.mark.asyncio
async def test_사용자_위치에_따라_최근접_기관이_달라진다():
    seoul = await _interactor().execute(
        CorporateGuideQuery(user_id="u1", latitude=_SEOUL[0], longitude=_SEOUL[1])
    )
    jeonju = await _interactor().execute(
        CorporateGuideQuery(user_id="u1", latitude=_JEONJU[0], longitude=_JEONJU[1])
    )

    seoul_tax = next(t for t in seoul.tasks if t.task_name == "사업자등록").institutions[0].name
    jeonju_tax = next(t for t in jeonju.tasks if t.task_name == "사업자등록").institutions[0].name
    assert seoul_tax == "종로세무서"
    assert jeonju_tax == "전주세무서"


@pytest.mark.asyncio
async def test_부동산_담보대출_주제는_담보대출_서류를_안내한다():
    view = await _interactor().execute(
        CorporateGuideQuery(
            user_id="u1", latitude=_SEOUL[0], longitude=_SEOUL[1], topic="mortgage"
        )
    )
    task_names = [task.task_name for task in view.tasks]
    assert "부동산 등기부등본 발급" in task_names
    assert "담보 부동산 감정평가" in task_names
    # 법인 전용 업무는 담보대출 안내에 섞이지 않는다.
    assert "법인설립등기" not in task_names


@pytest.mark.asyncio
async def test_알_수_없는_주제는_법인_사무로_폴백한다():
    view = await _interactor().execute(
        CorporateGuideQuery(
            user_id="u1", latitude=_SEOUL[0], longitude=_SEOUL[1], topic="unknown"
        )
    )
    assert any(task.task_name == "사업자등록" for task in view.tasks)
