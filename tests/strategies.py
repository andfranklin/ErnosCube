from ErnosCube.orient_enum import OrientEnum
from ErnosCube.face_enum import FaceEnum
from ErnosCube.sticker import Sticker
from ErnosCube.face import Face

from hypothesis.strategies import sampled_from, builds, lists, one_of

orient_enums = sampled_from(list(OrientEnum.__members__.values()))
face_enums = sampled_from(list(FaceEnum.__members__.values()))
stickers = builds(Sticker, face_enums, orient_enums)


def generate_faces_strategy(n):
    sticker_row = lists(stickers, min_size=n, max_size=n)
    sticker_mat = lists(sticker_row, min_size=n, max_size=n)
    return builds(Face, sticker_mat)


faces_1 = generate_faces_strategy(1)
faces_2 = generate_faces_strategy(2)
faces_3 = generate_faces_strategy(3)
faces = one_of(faces_1, faces_2, faces_3)
