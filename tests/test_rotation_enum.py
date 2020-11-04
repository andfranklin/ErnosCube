from ErnosCube.rotation_enum import RotationEnum
from pytest import raises, mark


class TestAxisEnum:
    def test_get_enum(self):
        assert RotationEnum.get_enum("nothing") == RotationEnum.NOTHING
        assert RotationEnum.get_enum("NOTHING") == RotationEnum.NOTHING

        assert RotationEnum.get_enum("cw") == RotationEnum.CW
        assert RotationEnum.get_enum("CW") == RotationEnum.CW

        assert RotationEnum.get_enum("ccw") == RotationEnum.CCW
        assert RotationEnum.get_enum("CCW") == RotationEnum.CCW

        assert RotationEnum.get_enum("ht") == RotationEnum.HT
        assert RotationEnum.get_enum("HT") == RotationEnum.HT

    def test_get_enum_failure_1(self):
        with raises(Exception):
            RotationEnum.get_enum("a")

    @mark.dependency(name="items")
    def test_items(self):
        assert len(RotationEnum.items()) == 4

    def test_get_enum_failure_2(self):
        with raises(Exception):
            RotationEnum.get_enum([])

    @mark.dependency(depends=["items"])
    def test_get_enum_trivial(self):
        for _, enum in RotationEnum.items():
            assert RotationEnum.get_enum(enum) == enum
