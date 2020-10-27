from enum import Enum
from .rotatable import Rotatable, EnumABCMeta


class OrientEnum(Rotatable, Enum, metaclass=EnumABCMeta):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

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
