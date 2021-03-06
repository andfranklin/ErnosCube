from ErnosCube.orient_enum import OrientEnum
from ErnosCube.face_enum import FaceEnum
from ErnosCube.sticker import Sticker
from ErnosCube.cube import Cube
from ErnosCube.rotation_enum import RotationEnum
from ErnosCube.axis_enum import AxisEnum
from ErnosCube.cube_mutation import CubeMutation

from hypothesis.strategies import sampled_from, builds, one_of
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
cubes_2 = builds(Cube, integers(min_value=2, max_value=2))

axis_enums = sampled_from(list(AxisEnum.__members__.values()))
rotation_enums = sampled_from(list(RotationEnum.__members__.values()))
layers = integers(min_value=-1)
cube_mutations = builds(CubeMutation, axis_enums, rotation_enums, layers)
