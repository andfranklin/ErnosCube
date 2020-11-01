from enum import Enum, auto
from dataclasses import dataclass


class AxisEnum(Enum):
    X = auto()
    Y = auto()
    Z = auto()


class MagEnum(Enum):
    CW = auto()
    CCW = auto()
    HT = auto()


@dataclass
class Rotation:
    axis: AxisEnum
    mag: MagEnum
    layer: int

    def __post_init__(self):
        assert self.layer >= -1
