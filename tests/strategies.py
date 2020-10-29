from ErnosCube.orient_enum import OrientEnum
from ErnosCube.face_enum import FaceEnum
from ErnosCube.sticker import Sticker
from ErnosCube.face import Face

from hypothesis.strategies import sampled_from, builds, lists, one_of, just

orient_enums = sampled_from(list(OrientEnum.__members__.values()))
face_enums = sampled_from(list(FaceEnum.__members__.values()))
stickers = builds(Sticker, face_enums, orient_enums)


def gen_faces_strategy(n):
    sticker_row = lists(stickers, min_size=n, max_size=n)
    sticker_mat = lists(sticker_row, min_size=n, max_size=n)
    return builds(Face, sticker_mat)


faces_1 = gen_faces_strategy(1)
faces_2 = gen_faces_strategy(2)
faces_3 = gen_faces_strategy(3)
faces = one_of(faces_1, faces_2, faces_3)


def gen_orthogonal(n, i):
    stickers = [
        [Sticker(FaceEnum.FRONT, OrientEnum.UP) for _ in range(n)] for _ in range(i)
    ]
    for _ in range(n - i):
        stickers.append([Sticker(FaceEnum.BACK, OrientEnum.DOWN) for _ in range(n)])
    return just(Face(stickers))


def gen_faces_minus_c2(n):
    return one_of(*[gen_orthogonal(n, i) for i in range(1, n)])


# all faces that do not have 180-degree symmetry
faces_minus_c2 = one_of(faces_1, gen_faces_minus_c2(2), gen_faces_minus_c2(3))


def gen_striped(n):
    build_uniform_sticker_rows = lambda s: lists(just(s), min_size=n, max_size=n)
    uniform_sticker_rows = stickers.flatmap(build_uniform_sticker_rows)
    uniform_sticker_mats = lists(uniform_sticker_rows, min_size=n, max_size=n)
    return builds(Face, uniform_sticker_mats)


def gen_c2_minus_c4_faces_4():
    stickers = [
        [
            Sticker(FaceEnum.BACK, OrientEnum.DOWN),
            Sticker(FaceEnum.FRONT, OrientEnum.UP),
            Sticker(FaceEnum.FRONT, OrientEnum.UP),
            Sticker(FaceEnum.BACK, OrientEnum.DOWN),
        ],
        [
            Sticker(FaceEnum.BACK, OrientEnum.DOWN),
            Sticker(FaceEnum.FRONT, OrientEnum.UP),
            Sticker(FaceEnum.FRONT, OrientEnum.UP),
            Sticker(FaceEnum.BACK, OrientEnum.DOWN),
        ],
        [
            Sticker(FaceEnum.BACK, OrientEnum.UP),
            Sticker(FaceEnum.FRONT, OrientEnum.DOWN),
            Sticker(FaceEnum.FRONT, OrientEnum.DOWN),
            Sticker(FaceEnum.BACK, OrientEnum.UP),
        ],
        [
            Sticker(FaceEnum.BACK, OrientEnum.UP),
            Sticker(FaceEnum.FRONT, OrientEnum.DOWN),
            Sticker(FaceEnum.FRONT, OrientEnum.DOWN),
            Sticker(FaceEnum.BACK, OrientEnum.UP),
        ],
    ]
    return just(Face(stickers))


_striped_faces = [gen_striped(i) for i in range(1, 3)]
c2_faces_minus_c4 = one_of(*_striped_faces, gen_c2_minus_c4_faces_4())
faces_minus_c4 = one_of(faces_minus_c2, c2_faces_minus_c4)
