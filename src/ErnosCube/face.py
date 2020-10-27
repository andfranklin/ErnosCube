from .sticker import Sticker
from .orient_enum import OrientEnum


class Face:
    """The face class for a Rubik's Cube.

    Every Rubik's Cube is made-up of 6 faces.
    """

    def __init__(self, stickers):
        self.N = len(stickers)
        assert all(len(row) == self.N for row in stickers)
        self.stickers = stickers


def construct_face_from_enum(face_enum, N=3):
    assert N > 0
    stickers = []
    for _ in range(N):
        stickers.append([Sticker(face_enum, OrientEnum.UP) for _ in range(N)])
    return Face(stickers)
