from ErnosCube.rotation import AxisEnum, MagEnum, Rotation
from strategies import axis_enums, mag_enums, layers, rotations
from hypothesis import given
from pytest import mark, raises
from copy import deepcopy


class TestRotation:
    """Collection of all tests run on instances of Rotation."""

    @mark.dependency(name="construction")
    @given(axis_enums, mag_enums, layers)
    def test_construction(self, axis, mag, layer):
        Rotation(axis, mag, layer)

    @mark.dependency(name="construction_failure", depends=["construction"])
    @given(axis_enums, mag_enums)
    def test_construction_failure(self, axis, mag):
        with raises(AssertionError):
            Rotation(axis, mag, -2)

    @mark.dependency(name="equality", depends=["construction_failure"])
    def test_equality(self):
        a = Rotation(AxisEnum.X, MagEnum.CW, 1)
        assert a == a

        b = Rotation(AxisEnum.X, MagEnum.CW, 2)
        assert not (a == b)

        c = Rotation(AxisEnum.X, MagEnum.CCW, 1)
        assert not (a == c)

        d = Rotation(AxisEnum.Y, MagEnum.CW, 1)
        assert not (a == d)

    @mark.dependency(name="inequality", depends=["equality"])
    @given(rotations, rotations)
    def test_inequality(self, a, b):
        if a == b:
            assert not (a != b)
        else:
            assert a != b

    @mark.dependency(name="deepcopy", depends=["equality"])
    @given(rotations)
    def test_deepcopy(self, rotation):
        rotation_copy = deepcopy(rotation)
        assert rotation is not rotation_copy
        assert rotation == rotation_copy
