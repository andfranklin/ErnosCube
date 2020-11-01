from ErnosCube.face import Face
from ErnosCube.face_enum import FaceEnum
from ErnosCube.orient_enum import OrientEnum
from ErnosCube.sticker import Sticker

from strategies import stickers, sticker_matrices
from utils import flatten, N_and_flatten
from hypothesis.strategies import builds, lists, one_of, just

face_from_sticker_matrix = lambda sm: Face(*N_and_flatten(sm))
faces = builds(face_from_sticker_matrix, sticker_matrices)


def gen_orthogonal(n, i):
    sticker_matrix = [
        [Sticker(FaceEnum.FRONT, OrientEnum.UP) for _ in range(n)] for _ in range(i)
    ]
    for _ in range(n - i):
        sticker_matrix.append(
            [Sticker(FaceEnum.BACK, OrientEnum.DOWN) for _ in range(n)]
        )
    return just(Face(n, flatten(sticker_matrix)))


def gen_faces_minus_c2(n):
    return one_of(*[gen_orthogonal(n, i) for i in range(1, n)])


faces_1 = builds(Face, just(1), stickers.flatmap(lambda s: just([s])))

# all faces that do not have 180-degree symmetry
faces_minus_c2 = one_of(faces_1, gen_faces_minus_c2(2), gen_faces_minus_c2(3))


def gen_striped(n):
    build_uniform_sticker_rows = lambda s: lists(just(s), min_size=n, max_size=n)
    uniform_sticker_rows = stickers.flatmap(build_uniform_sticker_rows)
    striped_sticker_mats = lists(uniform_sticker_rows, min_size=n, max_size=n)
    return builds(face_from_sticker_matrix, striped_sticker_mats)


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
    return just(Face(4, flatten(stickers)))


_striped_faces = [gen_striped(i) for i in range(1, 3)]
c2_faces_minus_c4 = one_of(*_striped_faces, gen_c2_minus_c4_faces_4())
faces_minus_c4 = one_of(faces_minus_c2, c2_faces_minus_c4)
