from ErnosCube.rotation_enum import RotationEnum
from pytest import raises


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

    def test_get_enum_failure(self):
        with raises(Exception):
            RotationEnum.get_enum("a")

    def test_items(self):
        assert len(RotationEnum.items()) == 4
