from ErnosCube.axis_enum import AxisEnum
from pytest import raises, mark


class TestAxisEnum:
    def test_get_enum(self):
        assert AxisEnum.get_enum("x") == AxisEnum.X
        assert AxisEnum.get_enum("X") == AxisEnum.X

        assert AxisEnum.get_enum("y") == AxisEnum.Y
        assert AxisEnum.get_enum("Y") == AxisEnum.Y

        assert AxisEnum.get_enum("z") == AxisEnum.Z
        assert AxisEnum.get_enum("Z") == AxisEnum.Z

    def test_get_enum_failure_1(self):
        with raises(Exception):
            AxisEnum.get_enum("a")

    def test_get_enum_failure_2(self):
        with raises(Exception):
            AxisEnum.get_enum([])

    @mark.dependency(name="items")
    def test_items(self):
        assert len(AxisEnum.items()) == 3

    @mark.dependency(depends=["items"])
    def test_get_enum_trivial(self):
        for _, enum in AxisEnum.items():
            assert AxisEnum.get_enum(enum) == enum
