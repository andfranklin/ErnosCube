from enum import Enum, auto
from dataclasses import dataclass
from .mag_enum import MagEnum


class AxisEnum(Enum):
    X = auto()
    Y = auto()
    Z = auto()


@dataclass
class CubeRotation:
    axis: AxisEnum
    mag: MagEnum
    layer: int

    def __post_init__(self):
        assert self.layer >= -1
