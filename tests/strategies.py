from ErnosCube.orient_enum import OrientEnum
from ErnosCube.face_enum import FaceEnum
from ErnosCube.sticker import Sticker

from hypothesis.strategies import sampled_from, builds, lists, one_of, just

orient_enums = sampled_from(list(OrientEnum.__members__.values()))
face_enums = sampled_from(list(FaceEnum.__members__.values()))
stickers = builds(Sticker, face_enums, orient_enums)
