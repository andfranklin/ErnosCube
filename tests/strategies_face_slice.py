from strategies import sticker_lists
from hypothesis.strategies import builds
from ErnosCube.face_slices import RowFaceSlice, ColFaceSlice
from copy import deepcopy


def asym_slice_filter(x):
    first = x.stickers[0]
    last = deepcopy(x.stickers[-1])
    return x.N == 1 or first != last.rotate_ht()


row_face_slices = builds(RowFaceSlice, sticker_lists)
row_face_slices_minus_c2 = row_face_slices.filter(asym_slice_filter)
col_face_slices = builds(ColFaceSlice, sticker_lists)
col_face_slices_minus_c2 = col_face_slices.filter(asym_slice_filter)
