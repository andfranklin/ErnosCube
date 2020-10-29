from ErnosCube.face_enum import FaceEnum
from ErnosCube.face import Face, construct_face_from_enum

from plane_rotatable_tests import PlaneRotatableTests
from hypothesis import given, example
from hypothesis.strategies import data
from strategies import stickers, face_enums
from strategies import faces, faces_minus_c2, faces_minus_c4
from copy import deepcopy


class TestFace(PlaneRotatableTests):
    """Collection of all tests run on instances of the Face Class."""

    objs = faces
    objs_minus_c2 = faces_minus_c2
    objs_minus_c4 = faces_minus_c4

    @given(stickers)
    def test_construction_1(self, sticker):
        face = Face([[sticker]])
        assert face.N == 1

    @given(data())
    def test_construction_2(self, data):
        face = Face(
            [
                [data.draw(stickers), data.draw(stickers)],
                [data.draw(stickers), data.draw(stickers)],
            ]
        )
        assert face.N == 2

    @given(data())
    def test_construction_3(self, data):
        face = Face(
            [
                [data.draw(stickers), data.draw(stickers), data.draw(stickers)],
                [data.draw(stickers), data.draw(stickers), data.draw(stickers)],
                [data.draw(stickers), data.draw(stickers), data.draw(stickers)],
            ]
        )
        assert face.N == 3

    @given(face_enums)
    def test_construct_face_from_enum(self, face_enum):
        face = construct_face_from_enum(face_enum)
        assert face.N == 3
        for row in face.stickers:
            assert all(sticker.init_face_enum == face_enum for sticker in row)

    @given(faces)
    @example(construct_face_from_enum(FaceEnum.FRONT, N=3))
    def test_str(self, face):
        gold = f"Face(N={face.N})"
        assert str(face) == gold

    def test_repr(self):
        face = construct_face_from_enum(FaceEnum.FRONT, N=3)
        gold = "\x1b[7m\x1b[1m\x1b[32m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ \x1b[0m\n\x1b[7m\x1b[1m\x1b[32m ↑"
        gold += " \x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ "
        gold += "\x1b[0m\n\x1b[7m\x1b[1m\x1b[32m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑"
        gold += " \x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ \x1b[0m"
        assert repr(face) == gold, repr(face)

    def test_get_raw_repr_size(self):
        face = construct_face_from_enum(FaceEnum.FRONT, N=3)
        assert face.get_raw_repr_size() == 9

    def test_rotate_cw(self):
        from ErnosCube.sticker import Sticker
        from ErnosCube.orient_enum import OrientEnum
        from ErnosCube.face_enum import FaceEnum

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

        assert comp_face.rotate_cw() == cw_comp_face

    def test_rotate_ccw(self):
        from ErnosCube.sticker import Sticker
        from ErnosCube.orient_enum import OrientEnum
        from ErnosCube.face_enum import FaceEnum

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

        assert comp_face.rotate_ccw() == ccw_comp_face

    def test_rotate_ht(self):
        from ErnosCube.sticker import Sticker
        from ErnosCube.orient_enum import OrientEnum
        from ErnosCube.face_enum import FaceEnum

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

        assert comp_face.rotate_ht() == ht_comp_face
