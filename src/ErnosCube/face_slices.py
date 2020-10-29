from .plane_rotatable import PlaneRotatable
from abc import abstractmethod


class FaceSlice(PlaneRotatable):
    """Base class for both the RowFaceSlice and ColFaceSlice."""

    def __init__(self, stickers):
        super().__init__()
        self.N = len(stickers)
        assert self.N > 0
        self.stickers = stickers

    def __eq__(self, other):
        same_type = self.__class__ == other.__class__
        els_eq = all(s1 == s2 for s1, s2 in zip(self.stickers, other.stickers))
        return same_type and els_eq

    # @classmethod
    # @abstractmethod
    # def from_face(cls, face, indx):
    #     pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class RowFaceSlice(FaceSlice):
    # @classmethod
    # def from_face(cls, face, row_indx):
    #     assert row_indx >= 0 and row_indx < face.N
    #     return cls([sticker for sticker in face.stickers[row_indx]])

    def rotate_cw(self):
        new_s = [sticker.rotate_cw() for sticker in self.stickers]
        return ColFaceSlice(new_s)

    def rotate_ccw(self):
        new_s = [sticker.rotate_ccw() for sticker in reversed(self.stickers)]
        return ColFaceSlice(new_s)

    def rotate_ht(self):
        new_s = [sticker.rotate_ht() for sticker in reversed(self.stickers)]
        return RowFaceSlice(new_s)

    def __str__(self):
        return f"RowFaceSlice(N={self.N})"

    def __repr__(self):
        return "".join(repr(sticker) for sticker in self.stickers)


class ColFaceSlice(FaceSlice):
    #     @classmethod
    #     def from_face(cls, face, col_indx):
    #         assert col_indx >= 0 and col_indx < face.N
    #         stickers = []
    #         for row in face.stickers:
    #             stickers.append(row[col_indx])
    #         return cls(stickers)

    def rotate_cw(self):
        new_s = [sticker.rotate_cw() for sticker in reversed(self.stickers)]
        return RowFaceSlice(new_s)

    def rotate_ccw(self):
        new_s = [sticker.rotate_ccw() for sticker in self.stickers]
        return RowFaceSlice(new_s)

    def rotate_ht(self):
        new_s = [sticker.rotate_ht() for sticker in reversed(self.stickers)]
        return ColFaceSlice(new_s)

    def __str__(self):
        return f"ColFaceSlice(N={self.N})"

    def __repr__(self):
        return "\n".join(repr(sticker) for sticker in self.stickers)
