from enum import Enum, auto


class RotationEnum(Enum):
    NOTHING = auto()
    CW = auto()
    CCW = auto()
    HT = auto()

    @staticmethod
    def get_enum(thing):
        if isinstance(thing, RotationEnum):
            return thing
        elif isinstance(thing, str):
            return RotationEnum[thing.upper()]
        else:
            err_str = f"Unable to coerce {thing} into a RotationEnum."
            raise Exception(err_str)

    @staticmethod
    def items():
        return RotationEnum.__members__.items()
