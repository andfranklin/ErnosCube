from .face_enum import FaceEnum
from .face import Face
from .sticker import Sticker
from .orient_enum import OrientEnum


class Cube:
    """An abstraction of a Rubik's Cube.

    Enables cube manipulations, and keeps track of sticker locations and
    Orientations.

    ----
    Initialize with arguments:
    - `N`, the side length (the cube is `N`x`N`x`N`)
    """

    def __init__(self, N=3):
        assert N > 0
        self.N = N
        self.last_layer = N - 1
        self.stickers = []
        self.faces = {}

        for face_indx, (_, face_enum) in enumerate(FaceEnum.items()):
            face_stickers = []
            for i in range(self.N):
                sticker_row = []
                for j in range(self.N):
                    sticker = Sticker(face_enum, OrientEnum.UP)
                    self.stickers.append(sticker)
                    sticker_row.append(sticker)  # this would be a pointer in C.
                face_stickers.append(sticker_row)
            self.faces[face_enum] = Face(face_stickers)

    def get_face(self, thing):
        enum = FaceEnum.get_enum(thing)
        return self.faces[enum]

    def __str__(self):
        return f"Cube(N={self.N})"

    def _generate_repr_lines(self):
        up_face = self.get_face("up")
        padding = up_face.get_raw_repr_size() * " "
        for row in up_face._generate_repr_lines():
            yield padding + row

        all_gens = [
            self.get_face(face)._generate_repr_lines()
            for face in ["left", "front", "right", "back"]
        ]
        for all_rows in zip(*all_gens):
            yield "".join(list(all_rows))

        for row in self.get_face("down")._generate_repr_lines():
            yield padding + row

    def __repr__(self):
        return "\n".join(self._generate_repr_lines())
