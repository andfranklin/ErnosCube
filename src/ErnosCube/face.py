from .orient_enum import OrientEnum
from .plane_rotatable import PlaneRotatable
from .face_slices import RowFaceSlice, ColFaceSlice


class Face(PlaneRotatable):
    """The face class for a Rubik's Cube.

    Every Rubik's Cube is made-up of 6 faces.
    """

    def __init__(self, N, stickers):
        super().__init__()
        assert N > 0
        N_sqrd = N * N
        assert len(stickers) == N_sqrd
        self.N = N

        # "pointer" to array of "pointers" to stickers.
        # These are owned by this Face.
        self.stickers = stickers

        # Cache of sticker "pointers" not owned by this Face.
        # Used in rotations. Avoids cache thrashing caused by
        # repeatedly allocating and deallocating arrays of
        # sticker pointers. Subject to redesign.
        self._sticker_cache = [None for _ in range(N_sqrd)]

    def __str__(self):
        return f"Face(N={self.N})"

    def _generate_repr_lines(self):
        for i in range(self.N):
            row = self.stickers[i : i + self.N]
            yield "".join(repr(sticker) for sticker in row)

    def __repr__(self):
        return "\n".join(self._generate_repr_lines())

    def get_raw_repr_size(self):
        return self.N * self.stickers[0].get_raw_repr_size()

    def __eq__(self, other):
        if self is other:
            return True

        if self.N != other.N:
            return False

        return all(a == b for a, b in zip(self.stickers, other.stickers))

    def _get_sticker_indx(self, row_indx, col_indx):
        return (self.N * row_indx) + col_indx

    def __getitem__(self, items):
        row_indx = items[0]
        col_indx = items[1]
        assert row_indx >= 0 and row_indx < self.N
        assert col_indx >= 0 and col_indx < self.N
        sticker_indx = self._get_sticker_indx(row_indx, col_indx)
        return self.stickers[sticker_indx]

    def rotate_cw(self):
        old_stickers = self.stickers
        new_stickers = self._sticker_cache
        for old_row in range(self.N):
            new_col = (self.N - 1) - old_row
            for old_col in range(self.N):
                new_row = old_col
                old_indx = self._get_sticker_indx(old_row, old_col)
                new_indx = self._get_sticker_indx(new_row, new_col)
                sticker = old_stickers[old_indx].rotate_cw()
                new_stickers[new_indx] = sticker
        self.stickers = new_stickers
        self._sticker_cache = old_stickers
        return self

    def rotate_ccw(self):
        old_stickers = self.stickers
        new_stickers = self._sticker_cache
        for old_row in range(self.N):
            new_col = old_row
            for old_col in range(self.N):
                new_row = (self.N - 1) - old_col
                old_indx = self._get_sticker_indx(old_row, old_col)
                new_indx = self._get_sticker_indx(new_row, new_col)
                sticker = old_stickers[old_indx].rotate_ccw()
                new_stickers[new_indx] = sticker
        self.stickers = new_stickers
        self._sticker_cache = old_stickers
        return self

    def rotate_ht(self):
        old_stickers = self.stickers
        new_stickers = self._sticker_cache
        for old_row in range(self.N):
            new_row = (self.N - 1) - old_row
            for old_col in range(self.N):
                new_col = (self.N - 1) - old_col
                old_indx = self._get_sticker_indx(old_row, old_col)
                new_indx = self._get_sticker_indx(new_row, new_col)
                sticker = old_stickers[old_indx].rotate_ht()
                new_stickers[new_indx] = sticker
        self.stickers = new_stickers
        self._sticker_cache = old_stickers
        return self

    def get_row_slice(self, row_indx):
        assert row_indx >= 0 and row_indx < self.N
        stickers = [None for _ in range(self.N)]
        for col_indx in range(self.N):
            sticker_indx = self._get_sticker_indx(row_indx, col_indx)
            stickers[col_indx] = self.stickers[sticker_indx]
        return RowFaceSlice(stickers)

    def get_col_slice(self, col_indx):
        assert col_indx >= 0 and col_indx < self.N
        stickers = [None for _ in range(self.N)]
        for row_indx in range(self.N):
            sticker_indx = self._get_sticker_indx(row_indx, col_indx)
            stickers[row_indx] = self.stickers[sticker_indx]
        return ColFaceSlice(stickers)

    def apply_slice(self, slice, indx):
        if isinstance(slice, RowFaceSlice):
            for col_indx, sticker in enumerate(slice.stickers):
                sticker_indx = self._get_sticker_indx(indx, col_indx)
                self.stickers[sticker_indx] = sticker

        else:
            for row_indx, sticker in enumerate(slice.stickers):
                sticker_indx = self._get_sticker_indx(row_indx, indx)
                self.stickers[sticker_indx] = sticker
