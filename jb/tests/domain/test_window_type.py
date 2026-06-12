from __future__ import annotations

from jb.shared_kernel.value_objects import WindowType, window_type_from_code


def test_일반_창구는_접두_없이_번호만():
    assert WindowType.GENERAL.format_ticket(3) == "3"


def test_법인_창구는_B_접두가_붙는다():
    assert WindowType.CORPORATE.format_ticket(3) == "B3"


def test_코드_문자열을_창구_종류로_해석한다():
    assert window_type_from_code("corporate") is WindowType.CORPORATE
    assert window_type_from_code("general") is WindowType.GENERAL


def test_알_수_없는_코드는_일반_창구로_본다():
    assert window_type_from_code("") is WindowType.GENERAL
    assert window_type_from_code("unknown") is WindowType.GENERAL
