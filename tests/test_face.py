from ErnosCube.face_enum import FaceEnum
from ErnosCube.orient_enum import OrientEnum
from ErnosCube.sticker import Sticker
from ErnosCube.face import Face
from ErnosCube.face import RowFaceSlice, ColFaceSlice

from plane_rotatable_tests import PlaneRotatableTests
from hypothesis import given, example
from hypothesis.strategies import data
from strategies import face_enums, stickers, sticker_matrices
from strategies_face import faces, faces_minus_c2, faces_minus_c4
from copy import deepcopy
from pytest import mark


class TestFace(PlaneRotatableTests):
    """Collection of all tests run on instances of the Face Class."""

    objs = faces
    objs_minus_c2 = faces_minus_c2
    objs_minus_c4 = faces_minus_c4

    @given(sticker_matrices)
    def construction_test(self, sticker_matrix):
        face = Face(sticker_matrix)
        assert face.N == len(sticker_matrix)

    @mark.dependency(name="construction_from_face_enum", depends=["construction"])
    @given(face_enums)
    def test_construction_from_face_enum(self, face_enum):
        face = Face.from_face_enum(face_enum)
        assert face.N == 3
        for row in face.stickers:
            assert all(sticker.init_face_enum == face_enum for sticker in row)

    @mark.dependency(depends=["construction_from_face_enum"])
    @given(faces)
    @example(Face.from_face_enum(FaceEnum.FRONT, N=3))
    def test_str(self, face):
        gold = f"Face(N={face.N})"
        assert str(face) == gold

    @mark.dependency(depends=["construction_from_face_enum"])
    def test_repr(self):
        face = Face.from_face_enum(FaceEnum.FRONT, N=3)
        gold = "\x1b[7m\x1b[1m\x1b[32m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ \x1b[0m\n\x1b[7m\x1b[1m\x1b[32m ↑"
        gold += " \x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ "
        gold += "\x1b[0m\n\x1b[7m\x1b[1m\x1b[32m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑"
        gold += " \x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ \x1b[0m"
        assert repr(face) == gold, f"{repr(face)}: {repr(repr(face))}"

    @mark.dependency(depends=["construction_from_face_enum"])
    def test_get_raw_repr_size(self):
        face = Face.from_face_enum(FaceEnum.FRONT, N=3)
        assert face.get_raw_repr_size() == 9

    def rotate_cw_test(self):
        stickers = []

        s00 = Sticker(FaceEnum.FRONT, OrientEnum.UP)
        s01 = Sticker(FaceEnum.RIGHT, OrientEnum.RIGHT)
        s02 = Sticker(FaceEnum.BACK, OrientEnum.DOWN)
        stickers.append([s00, s01, s02])

        s10 = Sticker(FaceEnum.LEFT, OrientEnum.LEFT)
        s11 = Sticker(FaceEnum.UP, OrientEnum.UP)
        s12 = Sticker(FaceEnum.DOWN, OrientEnum.RIGHT)
        stickers.append([s10, s11, s12])

        s20 = Sticker(FaceEnum.FRONT, OrientEnum.DOWN)
        s21 = Sticker(FaceEnum.RIGHT, OrientEnum.LEFT)
        s22 = Sticker(FaceEnum.BACK, OrientEnum.UP)
        stickers.append([s20, s21, s22])

        comp_face = Face(stickers)

        cw_stickers = []

        sticker_row = [s20, s10, s00]
        cw_stickers.append([deepcopy(s).rotate_cw() for s in sticker_row])

        sticker_row = [s21, s11, s01]
        cw_stickers.append([deepcopy(s).rotate_cw() for s in sticker_row])

        sticker_row = [s22, s12, s02]
        cw_stickers.append([deepcopy(s).rotate_cw() for s in sticker_row])

        cw_comp_face = Face(cw_stickers)

        assert (
            comp_face.rotate_cw() == cw_comp_face
        ), f"failed for {str(comp_face)}\n{repr(comp_face)}"

    def rotate_ccw_test(self):
        ccw_stickers = []

        s00 = Sticker(FaceEnum.FRONT, OrientEnum.UP)
        s01 = Sticker(FaceEnum.RIGHT, OrientEnum.RIGHT)
        s02 = Sticker(FaceEnum.BACK, OrientEnum.DOWN)
        ccw_stickers.append([s00, s01, s02])

        s10 = Sticker(FaceEnum.LEFT, OrientEnum.LEFT)
        s11 = Sticker(FaceEnum.UP, OrientEnum.UP)
        s12 = Sticker(FaceEnum.DOWN, OrientEnum.RIGHT)
        ccw_stickers.append([s10, s11, s12])

        s20 = Sticker(FaceEnum.FRONT, OrientEnum.DOWN)
        s21 = Sticker(FaceEnum.RIGHT, OrientEnum.LEFT)
        s22 = Sticker(FaceEnum.BACK, OrientEnum.UP)
        ccw_stickers.append([s20, s21, s22])

        ccw_comp_face = Face(ccw_stickers)

        stickers = []

        sticker_row = [s20, s10, s00]
        stickers.append([deepcopy(s).rotate_cw() for s in sticker_row])

        sticker_row = [s21, s11, s01]
        stickers.append([deepcopy(s).rotate_cw() for s in sticker_row])

        sticker_row = [s22, s12, s02]
        stickers.append([deepcopy(s).rotate_cw() for s in sticker_row])

        comp_face = Face(stickers)

        assert (
            comp_face.rotate_ccw() == ccw_comp_face
        ), f"failed for {str(comp_face)}\n{repr(comp_face)}"

    def rotate_ht_test(self):
        stickers = []

        s00 = Sticker(FaceEnum.FRONT, OrientEnum.UP)
        s01 = Sticker(FaceEnum.RIGHT, OrientEnum.RIGHT)
        s02 = Sticker(FaceEnum.BACK, OrientEnum.DOWN)
        stickers.append([s00, s01, s02])

        s10 = Sticker(FaceEnum.LEFT, OrientEnum.LEFT)
        s11 = Sticker(FaceEnum.UP, OrientEnum.UP)
        s12 = Sticker(FaceEnum.DOWN, OrientEnum.RIGHT)
        stickers.append([s10, s11, s12])

        s20 = Sticker(FaceEnum.FRONT, OrientEnum.DOWN)
        s21 = Sticker(FaceEnum.RIGHT, OrientEnum.LEFT)
        s22 = Sticker(FaceEnum.BACK, OrientEnum.UP)
        stickers.append([s20, s21, s22])

        comp_face = Face(stickers)

        ht_stickers = []

        sticker_row = [s22, s21, s20]
        ht_stickers.append([deepcopy(s).rotate_ht() for s in sticker_row])

        sticker_row = [s12, s11, s10]
        ht_stickers.append([deepcopy(s).rotate_ht() for s in sticker_row])

        sticker_row = [s02, s01, s00]
        ht_stickers.append([deepcopy(s).rotate_ht() for s in sticker_row])

        ht_comp_face = Face(ht_stickers)

        assert (
            comp_face.rotate_ht() == ht_comp_face
        ), f"failed for {str(comp_face)}\n{repr(comp_face)}"

    def stickers_and_face(self):
        s1 = Sticker(FaceEnum.FRONT, OrientEnum.UP)
        s2 = Sticker(FaceEnum.BACK, OrientEnum.RIGHT)
        s3 = Sticker(FaceEnum.LEFT, OrientEnum.DOWN)
        stickers = [s1, s2, s3]

        cs = Sticker(FaceEnum.RIGHT, OrientEnum.LEFT)
        face_stickers = []
        face_stickers.append([cs, s1, cs])
        face_stickers.append([s1, s2, s3])
        face_stickers.append([cs, s3, cs])
        return stickers, Face(face_stickers)

    @mark.dependency(name="get_row_slice", depends=["construction"])
    def test_get_row_slice(self):
        stickers, face = self.stickers_and_face()
        face_slice = face.get_row_slice(1)
        assert isinstance(face_slice, RowFaceSlice)
        assert all(a == b for a, b in zip(face_slice.stickers, stickers))

    @mark.dependency(name="get_col_slice", depends=["construction"])
    def test_get_col_slice(self):
        stickers, face = self.stickers_and_face()
        face_slice = face.get_col_slice(1)
        assert isinstance(face_slice, ColFaceSlice)
        assert all(a == b for a, b in zip(face_slice.stickers, stickers))

    @mark.dependency(depends=["get_row_slice"])
    def test_apply_row_slice(self):
        stickers, face = self.stickers_and_face()
        face_slice = face.get_row_slice(1)
        face.apply_slice(face_slice, 0)
        assert all(
            a == b for a, b in zip(face.stickers[0], stickers)
        ), f"\n{repr(face)}"

    @mark.dependency(depends=["get_col_slice"])
    def test_apply_col_slice(self):
        stickers, face = self.stickers_and_face()
        face_slice = face.get_col_slice(1)
        face.apply_slice(face_slice, 0)
        for i, row in enumerate(face.stickers):
            assert row[0] == stickers[i], f"\n{repr(face)}"
