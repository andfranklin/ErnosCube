from .plane_rotatable import PlaneRotatable
from termcolor import colored


class Sticker(PlaneRotatable):
    """The sticker class for a Rubik's Cube.

    The face of every Rubik's Cube is made-up of a bunch of stickers. 
    """

    def __init__(self, init_face_enum, orient_enum):
        self.init_face_enum = init_face_enum
        self.orient_enum = orient_enum

    def rotate_cw(self):
        self.orient_enum = self.orient_enum.rotate_cw()
        return self

    def rotate_ccw(self):
        self.orient_enum = self.orient_enum.rotate_ccw()
        return self

    def rotate_ht(self):
        self.orient_enum = self.orient_enum.rotate_ht()
        return self

    def __str__(self):
        return f"Sticker({self.init_face_enum}, {self.orient_enum})"

    def _get_raw_repr(self):
        return f" {repr(self.orient_enum)} "

    def get_raw_repr_size(self):
        return len(self._get_raw_repr())

    def __repr__(self):
        color = self.init_face_enum.get_terminal_color()
        attrs = ['bold', 'reverse']
        raw_repr = self._get_raw_repr()
        return colored(raw_repr, color, attrs=attrs)

    def __eq__(self, other):
        same_face = self.init_face_enum == other.init_face_enum
        same_orient = self.orient_enum == other.orient_enum
        return same_face and same_orient