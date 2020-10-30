from .sticker import Sticker
from .orient_enum import OrientEnum
from .plane_rotatable import PlaneRotatable
from .face_slices import RowFaceSlice, ColFaceSlice


class Face(PlaneRotatable):
    """The face class for a Rubik's Cube.

    Every Rubik's Cube is made-up of 6 faces.
    """

    def __init__(self, stickers):
        super().__init__()
        self.N = len(stickers)
        assert self.N > 0
        assert all(len(row) == self.N for row in stickers)
        self.stickers = stickers

    @classmethod
    def from_face_enum(cls, face_enum, N=3):
        assert N > 0
        stickers = []
        for _ in range(N):
            stickers.append([Sticker(face_enum, OrientEnum.UP) for _ in range(N)])
        return cls(stickers)

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
        if self.N != other.N:
            return False

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

    def get_row_slice(self, indx):
        assert indx >= 0 and indx < self.N
        return RowFaceSlice([sticker for sticker in self.stickers[indx]])

    def get_col_slice(self, indx):
        assert indx >= 0 and indx < self.N
        stickers = []
        for row in self.stickers:
            stickers.append(row[indx])
        return ColFaceSlice(stickers)

    def apply_slice(self, slice, indx):
        stickers = self.stickers

        if isinstance(slice, RowFaceSlice):
            row = stickers[indx]
            for j, sticker in enumerate(slice.stickers):
                row[j] = sticker

        else:
            for i, sticker in enumerate(slice.stickers):
                stickers[i][indx] = sticker
