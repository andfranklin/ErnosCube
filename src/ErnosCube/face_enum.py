from enum import Enum


class FaceEnum(Enum):
    """An Enum describing the face of a cube.

    This is used in two locations: 1) in stickers it is used to
    mark the initial face that they belong to, 2) in the cube
    to manage the faces.
    """

    FRONT = 0  # classically green
    RIGHT = 1  # classically red
    BACK = 2  # classically yellow
    LEFT = 3  # classically orange
    UP = 4  # classically white
    DOWN = 5  # classically blue

    @staticmethod
    def get_enum(thing):
        if isinstance(thing, FaceEnum):
            return thing
        elif isinstance(thing, str):
            return FaceEnum[thing.upper()]
        elif isinstance(thing, int):
            return FaceEnum(thing)
        else:
            err_str = f"Unable to coerce {thing} into a FaceEnum."
            raise Exception(err_str)

    @staticmethod
    def get_int(thing):
        return FaceEnum.get_enum(thing).value

    @staticmethod
    def get_str(thing):
        return FaceEnum.get_enum(thing).name

    @staticmethod
    def items():
        return FaceEnum.__members__.items()

    def get_terminal_color(self):
        if self == FaceEnum.FRONT:
            return "green"
        elif self == FaceEnum.RIGHT:
            return "red"
        elif self == FaceEnum.BACK:
            return "yellow"
        elif self == FaceEnum.LEFT:
            return "magenta"
        elif self == FaceEnum.UP:
            return "white"
        else:
            return "blue"
