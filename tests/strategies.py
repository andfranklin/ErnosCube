from ErnosCube.orient_enum import OrientEnum
from ErnosCube.face_enum import FaceEnum
from ErnosCube.sticker import Sticker
from ErnosCube.cube import Cube

from hypothesis.strategies import sampled_from, builds, one_of, just
from hypothesis.strategies import lists, integers

orient_enums = sampled_from(list(OrientEnum.__members__.values()))
face_enums = sampled_from(list(FaceEnum.__members__.values()))
stickers = builds(Sticker, face_enums, orient_enums)
sticker_lists = lists(stickers, min_size=1, max_size=3)


def gen_sticker_matrix(n):
    sticker_row = lists(stickers, min_size=n, max_size=n)
    return lists(sticker_row, min_size=n, max_size=n)


sticker_matrices = one_of(gen_sticker_matrix(i) for i in range(1, 3))
cubes = builds(Cube, integers(min_value=1, max_value=5))
