from enum import Enum, auto
from dataclasses import dataclass
from .rotation_enum import RotationEnum


class AxisEnum(Enum):
    X = auto()
    Y = auto()
    Z = auto()


@dataclass
class CubeRotation:
    axis: AxisEnum
    rotation_enum: RotationEnum
    layer: int

    def __post_init__(self):
        assert self.layer >= -1
