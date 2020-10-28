from enum import Enum
from .plane_rotatable import PlaneRotatable
from .enum_abc_meta import EnumABCMeta


class OrientEnum(PlaneRotatable, Enum, metaclass=EnumABCMeta):
    """An Enum describing the orientation of a sticker."""

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __eq__(self, other):
        return super(Enum).__eq__(other)

    def rotate_cw(self):
        if self == OrientEnum.UP:
            return OrientEnum.RIGHT
        elif self == OrientEnum.RIGHT:
            return OrientEnum.DOWN
        elif self == OrientEnum.DOWN:
            return OrientEnum.LEFT
        else:
            return OrientEnum.UP

    def rotate_ccw(self):
        if self == OrientEnum.UP:
            return OrientEnum.LEFT
        elif self == OrientEnum.RIGHT:
            return OrientEnum.UP
        elif self == OrientEnum.DOWN:
            return OrientEnum.RIGHT
        else:
            return OrientEnum.DOWN

    def rotate_ht(self):
        if self == OrientEnum.UP:
            return OrientEnum.DOWN
        elif self == OrientEnum.RIGHT:
            return OrientEnum.LEFT
        elif self == OrientEnum.DOWN:
            return OrientEnum.UP
        else:
            return OrientEnum.RIGHT

    def __repr__(self):
        if self == OrientEnum.UP:
            return "↑"
        elif self == OrientEnum.RIGHT:
            return "→"
        elif self == OrientEnum.DOWN:
            return "↓"
        else:
            return "←"
