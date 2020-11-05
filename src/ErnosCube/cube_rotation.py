from dataclasses import dataclass
from .axis_enum import AxisEnum
from .rotation_enum import RotationEnum


@dataclass
class CubeRotation:
    axis_enum: AxisEnum
    rotation_enum: RotationEnum
    layer: int

    def __post_init__(self):
        assert self.layer >= -1

    def inverse(self):
        if self.rotation_enum == RotationEnum.CW:
            opposite_rotation = RotationEnum.CCW
        elif self.rotation_enum == RotationEnum.CCW:
            opposite_rotation = RotationEnum.CW
        else:
            opposite_rotation = self.rotation_enum
        return CubeRotation(self.axis_enum, opposite_rotation, self.layer)


# The identity element
CubeRotation.e = CubeRotation(AxisEnum.NOTHING, RotationEnum.NOTHING, -1)
