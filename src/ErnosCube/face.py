from .sticker import Sticker
from .orient_enum import OrientEnum
from .plane_rotatable import PlaneRotatable


class Face(PlaneRotatable):
    """The face class for a Rubik's Cube.

    Every Rubik's Cube is made-up of 6 faces.
    """

    def __init__(self, stickers):
        self.N = len(stickers)
        assert self.N > 0
        assert all(len(row) == self.N for row in stickers)
        self.stickers = stickers

    def __str__(self):
        return f"Face(N={self.N})"

    def _generate_repr_lines(self):
        for row in self.stickers:
            yield "".join(repr(sticker) for sticker in row)

    def __repr__(self):
        return "\n".join(self._generate_repr_lines())

    def get_raw_repr_size(self):
        return self.N * self.stickers[0][0].get_raw_repr_size()

    def __eq__(self, other):
        assert self.N == other.N
        for self_row, other_row in zip(self.stickers, other.stickers):
            if not all(a == b for a, b in zip(self_row, other_row)):
                return False
        return True

    def rotate_cw(self):
        new_stickers = [[None for _ in range(self.N)] for _ in range(self.N)]
        for old_row in range(self.N):
            new_col = (self.N - 1) - old_row
            for old_col in range(self.N):
                new_row = old_col
                sticker = self.stickers[old_row][old_col].rotate_cw()
                new_stickers[new_row][new_col] = sticker
        self.stickers = new_stickers
        return self

    def rotate_ccw(self):
        new_stickers = [[None for _ in range(self.N)] for _ in range(self.N)]
        for old_row in range(self.N):
            new_col = old_row
            for old_col in range(self.N):
                new_row = (self.N - 1) - old_col
                sticker = self.stickers[old_row][old_col].rotate_ccw()
                new_stickers[new_row][new_col] = sticker
        self.stickers = new_stickers
        return self

    def rotate_ht(self):
        new_stickers = [[None for _ in range(self.N)] for _ in range(self.N)]
        for old_row in range(self.N):
            new_row = (self.N - 1) - old_row
            for old_col in range(self.N):
                new_col = (self.N - 1) - old_col
                sticker = self.stickers[old_row][old_col].rotate_ht()
                new_stickers[new_row][new_col] = sticker
        self.stickers = new_stickers
        return self


def construct_face_from_enum(face_enum, N=3):
    assert N > 0
    stickers = []
    for _ in range(N):
        stickers.append([Sticker(face_enum, OrientEnum.UP) for _ in range(N)])
    return Face(stickers)
