from dataclasses import dataclass
from .axis_enum import AxisEnum
from .rotation_enum import RotationEnum


@dataclass
class CubeRotation:
    axis: AxisEnum
    rotation_enum: RotationEnum
    layer: int

    def __post_init__(self):
        assert self.layer >= -1
