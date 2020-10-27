from hypothesis.strategies import sampled_from

from ErnosCube.orient_enum import OrientEnum

orient_enums = sampled_from(list(OrientEnum.__members__.values()))