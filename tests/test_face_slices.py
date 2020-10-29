from ErnosCube.face_slices import RowFaceSlice, ColFaceSlice
from ErnosCube.sticker import Sticker
from ErnosCube.face_enum import FaceEnum
from ErnosCube.orient_enum import OrientEnum
from ErnosCube.face import Face

from plane_rotatable_tests import PlaneRotatableTests
from strategies_face_slice import sticker_lists
from strategies_face_slice import row_face_slices, row_face_slices_minus_c2
from strategies_face_slice import col_face_slices, col_face_slices_minus_c2

from copy import deepcopy
from pytest import mark, fixture
from hypothesis import given


class FaceSlicesTests(PlaneRotatableTests):
    """Collection of all tests run on all instances of the FaceSlices Class."""

    @mark.dependency(name="construction")
    @given(sticker_lists)
    def test_construction(self, sticker_list):
        face_slice = self.class_(sticker_list)
        assert face_slice.N == len(sticker_list)

    @fixture
    def stickers(self):
        s1 = Sticker(FaceEnum.FRONT, OrientEnum.UP)
        s2 = Sticker(FaceEnum.BACK, OrientEnum.RIGHT)
        s3 = Sticker(FaceEnum.LEFT, OrientEnum.DOWN)
        return [s1, s2, s3]

    @fixture
    def face(self, stickers):
        s1, s2, s3 = stickers
        cs = Sticker(FaceEnum.RIGHT, OrientEnum.LEFT)
        face_stickers = []
        face_stickers.append([cs, s1, cs])
        face_stickers.append([s1, s2, s3])
        face_stickers.append([cs, s3, cs])
        return Face(face_stickers)

    @mark.dependency(depends=["construction"])
    def test_construction_from_face(self, face, stickers):
        face_slice = self.class_.from_face(face, 1)
        assert all(a == b for a, b in zip(face_slice.stickers, stickers))


class TestRowFaceSlices(FaceSlicesTests):
    """Collection of all tests run on instances of the RowFaceSlices Class."""

    class_ = RowFaceSlice
    objs = row_face_slices
    objs_minus_c2 = row_face_slices_minus_c2
    objs_minus_c4 = row_face_slices

    @mark.dependency(depends=["construction"])
    def test_str(self, stickers):
        gold = f"RowFaceSlice(N=3)"
        assert str(RowFaceSlice(stickers)) == gold

    @mark.dependency(depends=["construction"])
    def test_repr(self, stickers):
        face = RowFaceSlice(stickers)
        gold = "\x1b[7m\x1b[1m\x1b[32m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[33m → "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[35m ↓ \x1b[0m"
        assert repr(face) == gold, f"{repr(face)}: {repr(repr(face))}"

    def test_rotate_cw(self, stickers):
        orig_slice = RowFaceSlice(stickers)
        face_slice = RowFaceSlice(deepcopy(stickers)).rotate_cw()
        assert isinstance(face_slice, ColFaceSlice)

        err_str = f"\n{repr(orig_slice)})\nto\n{repr(face_slice)}"
        sol_stickers = face_slice.stickers
        assert sol_stickers[0] == Sticker(FaceEnum.FRONT, OrientEnum.RIGHT), err_str
        assert sol_stickers[1] == Sticker(FaceEnum.BACK, OrientEnum.DOWN), err_str
        assert sol_stickers[2] == Sticker(FaceEnum.LEFT, OrientEnum.LEFT), err_str

    def test_rotate_ccw(self, stickers):
        orig_slice = RowFaceSlice(stickers)
        face_slice = RowFaceSlice(deepcopy(stickers)).rotate_ccw()
        assert isinstance(face_slice, ColFaceSlice)

        err_str = f"\n{repr(orig_slice)})\nto\n{repr(face_slice)}"
        sol_stickers = face_slice.stickers
        assert sol_stickers[0] == Sticker(FaceEnum.LEFT, OrientEnum.RIGHT), err_str
        assert sol_stickers[1] == Sticker(FaceEnum.BACK, OrientEnum.UP), err_str
        assert sol_stickers[2] == Sticker(FaceEnum.FRONT, OrientEnum.LEFT), err_str

    def test_rotate_ht(self, stickers):
        orig_slice = RowFaceSlice(stickers)
        face_slice = RowFaceSlice(deepcopy(stickers)).rotate_ht()
        assert isinstance(face_slice, RowFaceSlice)

        err_str = f"\n{repr(orig_slice)})\nto\n{repr(face_slice)}"
        sol_stickers = face_slice.stickers
        assert sol_stickers[0] == Sticker(FaceEnum.LEFT, OrientEnum.UP), err_str
        assert sol_stickers[1] == Sticker(FaceEnum.BACK, OrientEnum.LEFT), err_str
        assert sol_stickers[2] == Sticker(FaceEnum.FRONT, OrientEnum.DOWN), err_str
