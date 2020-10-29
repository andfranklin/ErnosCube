from ErnosCube.orient_enum import OrientEnum
from ErnosCube.face_enum import FaceEnum
from ErnosCube.sticker import Sticker

from hypothesis.strategies import sampled_from, builds, lists, one_of, just

orient_enums = sampled_from(list(OrientEnum.__members__.values()))
face_enums = sampled_from(list(FaceEnum.__members__.values()))
stickers = builds(Sticker, face_enums, orient_enums)


def gen_sticker_matrix(n):
    sticker_row = lists(stickers, min_size=n, max_size=n)
    return lists(sticker_row, min_size=n, max_size=n)


sticker_matrices = one_of(gen_sticker_matrix(i) for i in range(1, 3))
