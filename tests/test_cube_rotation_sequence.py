# from ErnosCube.axis_enum import AxisEnum
# from ErnosCube.rotation_enum import RotationEnum
# from ErnosCube.cube_rotation import CubeRotation
from ErnosCube.cube_rotation_sequence import CubeRotationSequence

from strategies import axis_enums, rotation_enums, layers, cube_rotations
from strategies import cube_rotation_lists, cube_rotation_sequences
from hypothesis import given
from pytest import mark, raises
from copy import deepcopy


class TestCubeRotationSequence:
    """Collection of all tests run on instances of CubeRotationSequence."""

    @mark.dependency(name="construction")
    @given(cube_rotation_lists)
    def test_construction(self, cube_rotation_list):
        CubeRotationSequence(*cube_rotation_list)

    @mark.dependency(name="append", depends=["construction"])
    @given(cube_rotation_sequences, cube_rotations)
    def test_append(self, cube_rotation_sequence, cube_rotation):
        n = len(cube_rotation_sequence.rotations)
        cube_rotation_sequence.append(cube_rotation)
        assert len(cube_rotation_sequence.rotations) == n + 1

    @mark.dependency(name="extend_1", depends=["construction"])
    @given(cube_rotation_sequences, cube_rotation_sequences)
    def test_extend_1(self, a, b):
        n_a = len(a.rotations)
        n_b = len(b.rotations)
        a.extend(b)
        assert len(a.rotations) == n_a + n_b
        for i, b_rotation in enumerate(b.rotations):
            a_rotation = a.rotations[n_a + i]
            assert a_rotation == b_rotation

    @mark.dependency(name="extend_2", depends=["construction"])
    @given(cube_rotation_sequences, cube_rotation_lists)
    def test_extend_2(self, crs, crl):
        n_crs = len(crs.rotations)
        n_crl = len(crl)
        crs.extend(crl)
        assert len(crs.rotations) == n_crs + n_crl
        for i, crl_rotation in enumerate(crl):
            crs_rotation = crs.rotations[n_crs + i]
            assert crs_rotation == crl_rotation

    @mark.dependency(name="add_1", depends=["construction"])
    @given(cube_rotation_sequences, cube_rotation_sequences)
    def test_add_1(self, a, b):
        n_a = len(a.rotations)
        n_b = len(b.rotations)
        c = a + b
        assert len(c.rotations) == n_a + n_b

        for a_rotation, c_rotation in zip(a.rotations, c.rotations[:n_a]):
            assert c_rotation == a_rotation

        for i, b_rotation in enumerate(b.rotations):
            c_rotation = c.rotations[n_a + i]
            assert c_rotation == b_rotation

    @mark.dependency(name="add_2", depends=["construction"])
    @given(cube_rotation_sequences, cube_rotation_lists)
    def test_add_2(self, crs, crl):
        n_crs = len(crs.rotations)
        n_crl = len(crl)
        res = crs + crl
        assert len(res.rotations) == n_crs + n_crl

        for crs_rotation, res_rotation in zip(crs.rotations, res.rotations[:n_crs]):
            assert res_rotation == crs_rotation

        for i, crl_rotation in enumerate(crl):
            res_rotation = res.rotations[n_crs + i]
            assert res_rotation == crl_rotation

    @mark.dependency(name="add_3", depends=["construction"])
    @given(cube_rotation_sequences, cube_rotation_lists)
    def test_add_3(self, crs, crl):
        n_crs = len(crs.rotations)
        n_crl = len(crl)
        res = crl + crs
        assert len(res.rotations) == n_crs + n_crl

        for crl_rotation, res_rotation in zip(crl, res.rotations[:n_crl]):
            assert res_rotation == crl_rotation

        for i, crs_rotation in enumerate(crs.rotations):
            res_rotation = res.rotations[n_crl + i]
            assert res_rotation == crs_rotation
