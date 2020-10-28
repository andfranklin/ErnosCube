from ErnosCube.face import Face, construct_face_from_enum

from strategies import stickers, face_enums
from hypothesis.strategies import data
from hypothesis import given
from strategies import random_faces


class TestFace:
    """Collection of all tests run on instances of the Face Class."""

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

    @given(random_faces)
    def test_str(self, face):
        gold = f"Face(N={face.N})"
        assert str(face) == gold
