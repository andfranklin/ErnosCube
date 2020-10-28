from ErnosCube.orient_enum import OrientEnum
from ErnosCube.face_enum import FaceEnum
from ErnosCube.sticker import Sticker
from ErnosCube.face import Face

from hypothesis.strategies import sampled_from, builds, lists, one_of

orient_enums = sampled_from(list(OrientEnum.__members__.values()))
face_enums = sampled_from(list(FaceEnum.__members__.values()))
stickers = builds(Sticker, face_enums, orient_enums)


def generate_random_face_strategy(n):
    random_sticker_row = lists(stickers, min_size=n, max_size=n)
    random_sticker_mat = lists(random_sticker_row, min_size=n, max_size=n)
    return builds(Face, random_sticker_mat)


random_1_faces = generate_random_face_strategy(1)
random_2_faces = generate_random_face_strategy(2)
random_3_faces = generate_random_face_strategy(3)
random_faces = one_of(random_1_faces, random_2_faces, random_3_faces)
