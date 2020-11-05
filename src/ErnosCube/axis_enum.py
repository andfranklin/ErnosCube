from enum import Enum, auto


class AxisEnum(Enum):
    NOTHING = auto()
    X = auto()
    Y = auto()
    Z = auto()

    @staticmethod
    def get_enum(thing):
        if isinstance(thing, AxisEnum):
            return thing
        elif isinstance(thing, str):
            return AxisEnum[thing.upper()]
        else:
            err_str = f"Unable to coerce {thing} into a AxisEnum."
            raise Exception(err_str)

    @staticmethod
    def items():
        return AxisEnum.__members__.items()
