from ErnosCube.axis_enum import AxisEnum
from ErnosCube.rotation_enum import RotationEnum
from ErnosCube.cube_mutation import CubeMutation

from strategies import axis_enums, rotation_enums, layers, cube_mutations
from hypothesis import given
from pytest import mark, raises
from copy import deepcopy


class TestCubeMutation:
    """Collection of all tests run on instances of CubeMutation."""

    @mark.dependency(name="construction")
    @given(axis_enums, rotation_enums, layers)
    def test_construction(self, axis, mag, layer):
        CubeMutation(axis, mag, layer)

    @mark.dependency(name="construction_failure", depends=["construction"])
    @given(axis_enums, rotation_enums)
    def test_construction_failure(self, axis, mag):
        with raises(AssertionError):
            CubeMutation(axis, mag, -2)

    @mark.dependency(name="equality", depends=["construction_failure"])
    def test_equality(self):
        a = CubeMutation(AxisEnum.X, RotationEnum.CW, 1)
        assert a == a

        b = CubeMutation(AxisEnum.X, RotationEnum.CW, 2)
        assert not (a == b)

        c = CubeMutation(AxisEnum.X, RotationEnum.CCW, 1)
        assert not (a == c)

        d = CubeMutation(AxisEnum.Y, RotationEnum.CW, 1)
        assert not (a == d)

    @mark.dependency(name="inequality", depends=["equality"])
    @given(cube_mutations, cube_mutations)
    def test_inequality(self, a, b):
        if a == b:
            assert not (a != b)
        else:
            assert a != b

    @mark.dependency(name="deepcopy", depends=["equality"])
    @given(cube_mutations)
    def test_deepcopy(self, cube_mutation):
        mutation_copy = deepcopy(cube_mutation)
        assert cube_mutation is not mutation_copy
        assert cube_mutation == mutation_copy

    def test_inverse(self):
        for axis in [AxisEnum.X, AxisEnum.Y, AxisEnum.Z]:
            for layer in range(-1, 5):
                cw = CubeMutation(axis, RotationEnum.CW, layer)
                ccw = CubeMutation(axis, RotationEnum.CCW, layer)
                ht = CubeMutation(axis, RotationEnum.HT, layer)
                assert cw.inverse() == ccw
                assert ccw.inverse() == cw
                assert ht.inverse() == ht

        assert CubeMutation.e.inverse() == CubeMutation.e
