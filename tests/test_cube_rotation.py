from ErnosCube.cube_rotation import AxisEnum, CubeRotation
from ErnosCube.mag_enum import MagEnum
from strategies import axis_enums, mag_enums, layers, cube_rotations
from hypothesis import given
from pytest import mark, raises
from copy import deepcopy


class TestCubeRotation:
    """Collection of all tests run on instances of CubeRotation."""

    @mark.dependency(name="construction")
    @given(axis_enums, mag_enums, layers)
    def test_construction(self, axis, mag, layer):
        CubeRotation(axis, mag, layer)

    @mark.dependency(name="construction_failure", depends=["construction"])
    @given(axis_enums, mag_enums)
    def test_construction_failure(self, axis, mag):
        with raises(AssertionError):
            CubeRotation(axis, mag, -2)

    @mark.dependency(name="equality", depends=["construction_failure"])
    def test_equality(self):
        a = CubeRotation(AxisEnum.X, MagEnum.CW, 1)
        assert a == a

        b = CubeRotation(AxisEnum.X, MagEnum.CW, 2)
        assert not (a == b)

        c = CubeRotation(AxisEnum.X, MagEnum.CCW, 1)
        assert not (a == c)

        d = CubeRotation(AxisEnum.Y, MagEnum.CW, 1)
        assert not (a == d)

    @mark.dependency(name="inequality", depends=["equality"])
    @given(cube_rotations, cube_rotations)
    def test_inequality(self, a, b):
        if a == b:
            assert not (a != b)
        else:
            assert a != b

    @mark.dependency(name="deepcopy", depends=["equality"])
    @given(cube_rotations)
    def test_deepcopy(self, cube_rotation):
        rotation_copy = deepcopy(cube_rotation)
        assert cube_rotation is not rotation_copy
        assert cube_rotation == rotation_copy
