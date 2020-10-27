from hypothesis import given
from hypothesis.strategies import sampled_from

from ErnosCube.orient_enum import OrientEnum


def test_repr():
    assert repr(OrientEnum.UP) == "↑"
    assert repr(OrientEnum.DOWN) == "↓"
    assert repr(OrientEnum.LEFT) == "←"
    assert repr(OrientEnum.RIGHT) == "→"


def test_rotate_cw():
    assert OrientEnum.UP.rotate_cw() == OrientEnum.RIGHT
    assert OrientEnum.RIGHT.rotate_cw() == OrientEnum.DOWN
    assert OrientEnum.DOWN.rotate_cw() == OrientEnum.LEFT
    assert OrientEnum.LEFT.rotate_cw() == OrientEnum.UP


def test_rotate_ccw():
    assert OrientEnum.UP.rotate_ccw() == OrientEnum.LEFT
    assert OrientEnum.RIGHT.rotate_ccw() == OrientEnum.UP
    assert OrientEnum.DOWN.rotate_ccw() == OrientEnum.RIGHT
    assert OrientEnum.LEFT.rotate_ccw() == OrientEnum.DOWN


def test_rotate_ht():
    assert OrientEnum.UP.rotate_ht() == OrientEnum.DOWN
    assert OrientEnum.RIGHT.rotate_ht() == OrientEnum.LEFT
    assert OrientEnum.DOWN.rotate_ht() == OrientEnum.UP
    assert OrientEnum.LEFT.rotate_ht() == OrientEnum.RIGHT


all_orient_enums = list(OrientEnum.__members__.values())


@given(sampled_from(all_orient_enums))
def test_cw_ccw_invertability(enum):
    assert enum.rotate_cw().rotate_ccw() == enum
    assert enum.rotate_ccw().rotate_cw() == enum