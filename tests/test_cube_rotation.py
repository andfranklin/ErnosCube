from ErnosCube.cube_rotation import AxisEnum, CubeRotation
from ErnosCube.rotation_enum import RotationEnum
from strategies import axis_enums, rotation_enums, layers, cube_rotations
from hypothesis import given
from pytest import mark, raises
from copy import deepcopy


class TestCubeRotation:
    """Collection of all tests run on instances of CubeRotation."""

    @mark.dependency(name="construction")
    @given(axis_enums, rotation_enums, layers)
    def test_construction(self, axis, mag, layer):
        CubeRotation(axis, mag, layer)

    @mark.dependency(name="construction_failure", depends=["construction"])
    @given(axis_enums, rotation_enums)
    def test_construction_failure(self, axis, mag):
        with raises(AssertionError):
            CubeRotation(axis, mag, -2)

    @mark.dependency(name="equality", depends=["construction_failure"])
    def test_equality(self):
        a = CubeRotation(AxisEnum.X, RotationEnum.CW, 1)
        assert a == a

        b = CubeRotation(AxisEnum.X, RotationEnum.CW, 2)
        assert not (a == b)

        c = CubeRotation(AxisEnum.X, RotationEnum.CCW, 1)
        assert not (a == c)

        d = CubeRotation(AxisEnum.Y, RotationEnum.CW, 1)
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

    def test_inverse(self):
        for axis in [AxisEnum.X, AxisEnum.Y, AxisEnum.Z]:
            for layer in range(-1, 5):
                cw = CubeRotation(axis, RotationEnum.CW, layer)
                ccw = CubeRotation(axis, RotationEnum.CCW, layer)
                ht = CubeRotation(axis, RotationEnum.HT, layer)
                assert cw.inverse() == ccw
                assert ccw.inverse() == cw
                assert ht.inverse() == ht

        assert CubeRotation.e.inverse() == CubeRotation.e
