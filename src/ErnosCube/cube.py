from .face_enum import FaceEnum
from .face import Face
from .sticker import Sticker
from .orient_enum import OrientEnum


class Cube:
    """An abstraction of a Rubik's Cube.

    Enables cube manipulations, and keeps track of sticker locations and
    orientations. The list of stickers (`self.stickers`) is maintained
    only for memeory management of them (I know this isn't necessary for python.
    Eventually, I would like to port this code to Rust of C++ so I can get
    the speed of a compiled language that doesn't use garbage collection.
    I'm trying to account for memory management now, to make the transition
    easier later on). The faces (`self.faces`) are used to track their locations.

    ----
    Initialize with arguments:
    - `N`, the side length (the cube is `N`x`N`x`N`)
    """

    def __init__(self, N=3, init=True):
        assert N > 0
        self.N = N
        self.last_layer = N - 1
        self.stickers = []
        self.faces = {}

        # Dirty hack to implement the default initialization of a cube.
        # Would probably handle this differently in C++ or Rust.
        if init:
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

    @classmethod
    def from_faces(cls, faces):
        """Construct a cube from a provided dictionary of the faces.

        The cube takes ownership of the stickers from the faces.
        This method makes it easier to construct an arbitrary cube.

        Warning: there is not a check to ensure that the cube is solvable.
        This is by design.
        """
        assert len(faces) == 6
        cube = cls(N=faces[FaceEnum.FRONT].N, init=False)

        for enum, face in faces.items():
            assert face.N == cube.N
            cube.faces[enum] = face
            for row in face.stickers:
                cube.stickers.extend(row)
        return cube

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

    def __eq__(self, other):
        """Returns true iff the two cubes are strictly equal.

        Two cubes are strictly equal when each sticker on one cube
        corresponds to a sticker with the same location on the other cube,
        and each sticker has the same `init_face_enum` and `orient_enum`.
        """
        if self is other:
            return True

        if self.N != other.N:
            return False

        for face_enum, face in self.faces.items():
            other_face = other.faces[face_enum]
            if face != other_face:
                return False

        return True

    def __ne__(self, other):
        """Returns false iff the two cubes are strictly not equal."""
        return not (self == other)

    def _cw_rotation_x(self, layer):
        """Does a clockwise rotation of a given layer in the x-axis.

        The x-axis is orthogonal to the front and back faces. The positive
        direction of the x-axis is incident on the back face and exits the
        front face. The direction of rotation is defined with respect to
        the positive x-axis.
        """
        assert layer >= 0 and layer < self.N

        if layer == 0:
            back_face = self.faces[FaceEnum.BACK]
            back_face.rotate_cw()

        if layer == self.last_layer:
            front_face = self.faces[FaceEnum.FRONT]
            front_face.rotate_ccw()

        up_face = self.faces[FaceEnum.UP]
        up_index = layer
        up_slice = up_face.get_row_slice(up_index)
        up_slice = up_slice.rotate_ccw()

        left_face = self.faces[FaceEnum.LEFT]
        left_index = layer
        left_slice = left_face.get_col_slice(left_index)
        left_slice = left_slice.rotate_ccw()

        down_face = self.faces[FaceEnum.DOWN]
        down_index = self.last_layer - layer
        down_slice = down_face.get_row_slice(down_index)
        down_slice = down_slice.rotate_ccw()

        right_face = self.faces[FaceEnum.RIGHT]
        right_index = self.last_layer - layer
        right_slice = right_face.get_col_slice(right_index)
        right_slice = right_slice.rotate_ccw()

        up_face.apply_slice(right_slice, up_index)
        left_face.apply_slice(up_slice, left_index)
        down_face.apply_slice(left_slice, down_index)
        right_face.apply_slice(down_slice, right_index)
