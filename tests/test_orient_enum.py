from ErnosCube.orient_enum import OrientEnum
from plane_rotatable_tests import PlaneRotatableTests
from strategies import orient_enums


class TestOrientEnum(PlaneRotatableTests):
    objs = orient_enums
    objs_minus_c2 = orient_enums
    objs_minus_c4 = orient_enums

    def construction_test(self):
        pass  # Enums do no have constructors by default

    def test_repr(self):
        assert repr(OrientEnum.UP) == "↑"
        assert repr(OrientEnum.DOWN) == "↓"
        assert repr(OrientEnum.LEFT) == "←"
        assert repr(OrientEnum.RIGHT) == "→"

    def rotate_cw_test(self):
        assert OrientEnum.UP.rotate_cw() == OrientEnum.RIGHT
        assert OrientEnum.RIGHT.rotate_cw() == OrientEnum.DOWN
        assert OrientEnum.DOWN.rotate_cw() == OrientEnum.LEFT
        assert OrientEnum.LEFT.rotate_cw() == OrientEnum.UP

    def rotate_ccw_test(self):
        assert OrientEnum.UP.rotate_ccw() == OrientEnum.LEFT
        assert OrientEnum.RIGHT.rotate_ccw() == OrientEnum.UP
        assert OrientEnum.DOWN.rotate_ccw() == OrientEnum.RIGHT
        assert OrientEnum.LEFT.rotate_ccw() == OrientEnum.DOWN

    def rotate_ht_test(self):
        assert OrientEnum.UP.rotate_ht() == OrientEnum.DOWN
        assert OrientEnum.RIGHT.rotate_ht() == OrientEnum.LEFT
        assert OrientEnum.DOWN.rotate_ht() == OrientEnum.UP
        assert OrientEnum.LEFT.rotate_ht() == OrientEnum.RIGHT
