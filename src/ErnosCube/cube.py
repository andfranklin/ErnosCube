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

        # Slow and dynamic implementation for now.
        self.stickers = []
        self.faces = {}

        # Eventually, I'd like to massage this into something resembaling
        # a C/C++ or Rust implementation, like below.

        # self.faces = {enum: None for _, enum in FaceEnum.items()}
        # self.n_faces = len(self.faces)

        # self.n_stickers = self.n_faces * self.N * self.N
        # self.stickers = [None for _ in range(self.n_stickers)]

        # Dirty, but convenient in python.
        # I need to eventually change this.
        if init:
            self.init()

    def init(self):
        """Canonical initialization of a N x N x N Cube."""

        N_sqrd = self.N * self.N
        for face_indx, (_, face_enum) in enumerate(FaceEnum.items()):
            face_stickers = []
            for i in range(N_sqrd):
                sticker = Sticker(face_enum, OrientEnum.UP)
                self.stickers.append(sticker)
                face_stickers.append(sticker)
            self.faces[face_enum] = Face(self.N, face_stickers)

        # Eventually, I would like to construct the face. It would have a
        # static array of pointers to stickers. The stickers would be constructed
        # here, in Cube. Then the pointers in each face would point to these
        # stickers.

        # N_squared = self.N * self.N
        # for face_indx in range(self.n_faces):
        #     face_enum = FaceEnum.get_enum(face_indx)
        #     face_start = N_squared * face_indx
        #     face_stickers = [None for _ in range(self.N)]
        #     for i in range(self.N):
        #         row_start = self.N * i
        #         sticker_row = [None for _ in range(self.N)] # this would be a row of pointers in C.
        #         for j in range(self.N):
        #             stickers_indx = face_start + row_start + j
        #             self.stickers[stickers_indx] = Sticker(face_enum, OrientEnum.UP)
        #             sticker_row[j] = self.stickers[stickers_indx]
        #         face_stickers[i] = sticker_row
        #     self.faces[face_enum] = Face(face_stickers)

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
            cube.stickers.extend(face.stickers)

        # Eventually, I'd like to massage this into something resembling
        # a low-level implementation, like below. This will make
        # porting the code easier, and hopefully I'll have a good test
        # harness to ensure correctness.

        # N_squared = cube.N * cube.N
        # for face_indx, (face_enum, face) in enumerate(faces.items()):
        #     assert face.N == cube.N
        #     face_start = N_squared * face_indx
        #     cube.faces[face_enum] = face
        #     for row_indx, row in enumerate(face.stickers):
        #         row_start = cube.N * row_indx
        #         for col_indx, sticker in enumerate(row):
        #             stickers_indx = face_start + row_start + col_indx
        #             cube.stickers[stickers_indx] = sticker

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

    def _ccw_rotation_x(self, layer):
        """Does a counter-clockwise rotation of a given layer in the x-axis.

        The x-axis is orthogonal to the front and back faces. The positive
        direction of the x-axis is incident on the back face and exits the
        front face. The direction of rotation is defined with respect to
        the positive x-axis.
        """
        assert layer >= 0 and layer < self.N

        if layer == 0:
            back_face = self.faces[FaceEnum.BACK]
            back_face.rotate_ccw()

        if layer == self.last_layer:
            front_face = self.faces[FaceEnum.FRONT]
            front_face.rotate_cw()

        up_face = self.faces[FaceEnum.UP]
        up_index = layer
        up_slice = up_face.get_row_slice(up_index)
        up_slice = up_slice.rotate_cw()

        left_face = self.faces[FaceEnum.LEFT]
        left_index = layer
        left_slice = left_face.get_col_slice(left_index)
        left_slice = left_slice.rotate_cw()

        down_face = self.faces[FaceEnum.DOWN]
        down_index = self.last_layer - layer
        down_slice = down_face.get_row_slice(down_index)
        down_slice = down_slice.rotate_cw()

        right_face = self.faces[FaceEnum.RIGHT]
        right_index = self.last_layer - layer
        right_slice = right_face.get_col_slice(right_index)
        right_slice = right_slice.rotate_cw()

        up_face.apply_slice(left_slice, up_index)
        left_face.apply_slice(down_slice, left_index)
        down_face.apply_slice(right_slice, down_index)
        right_face.apply_slice(up_slice, right_index)

    def _ht_rotation_x(self, layer):
        """Does a half-turn rotation of a given layer in the x-axis.

        The x-axis is orthogonal to the front and back faces. The positive
        direction of the x-axis is incident on the back face and exits the
        front face. The direction of rotation is defined with respect to
        the positive x-axis.
        """
        assert layer >= 0 and layer < self.N

        if layer == 0:
            back_face = self.faces[FaceEnum.BACK]
            back_face.rotate_ht()

        if layer == self.last_layer:
            front_face = self.faces[FaceEnum.FRONT]
            front_face.rotate_ht()

        up_face = self.faces[FaceEnum.UP]
        up_index = layer
        up_slice = up_face.get_row_slice(up_index)
        up_slice = up_slice.rotate_ht()

        left_face = self.faces[FaceEnum.LEFT]
        left_index = layer
        left_slice = left_face.get_col_slice(left_index)
        left_slice = left_slice.rotate_ht()

        down_face = self.faces[FaceEnum.DOWN]
        down_index = self.last_layer - layer
        down_slice = down_face.get_row_slice(down_index)
        down_slice = down_slice.rotate_ht()

        right_face = self.faces[FaceEnum.RIGHT]
        right_index = self.last_layer - layer
        right_slice = right_face.get_col_slice(right_index)
        right_slice = right_slice.rotate_ht()

        up_face.apply_slice(down_slice, up_index)
        left_face.apply_slice(right_slice, left_index)
        down_face.apply_slice(up_slice, down_index)
        right_face.apply_slice(left_slice, right_index)

    def _cw_rotation_y(self, layer):
        """Does a clockwise rotation of a given layer in the y-axis.

        The y-axis is orthogonal to the front and back faces. The positive
        direction of the y-axis is incident on the left face and exits the
        right face. The direction of rotation is defined with respect to
        the positive y-axis.
        """
        assert layer >= 0 and layer < self.N

        if layer == 0:
            left_face = self.faces[FaceEnum.LEFT]
            left_face.rotate_cw()

        if layer == self.last_layer:
            right_face = self.faces[FaceEnum.RIGHT]
            right_face.rotate_ccw()

        up_face = self.faces[FaceEnum.UP]
        up_index = layer
        up_slice = up_face.get_col_slice(up_index)

        back_face = self.faces[FaceEnum.BACK]
        back_index = self.last_layer - layer
        back_slice = back_face.get_col_slice(back_index)
        back_slice = back_slice.rotate_ht()

        down_face = self.faces[FaceEnum.DOWN]
        down_index = layer
        down_slice = down_face.get_col_slice(down_index)
        down_slice = down_slice.rotate_ht()

        front_face = self.faces[FaceEnum.FRONT]
        front_index = layer
        front_slice = front_face.get_col_slice(front_index)

        up_face.apply_slice(back_slice, up_index)
        back_face.apply_slice(down_slice, back_index)
        down_face.apply_slice(front_slice, down_index)
        front_face.apply_slice(up_slice, front_index)

    def _ccw_rotation_y(self, layer):
        """Does a counter-clockwise rotation of a given layer in the y-axis.

        The y-axis is orthogonal to the front and back faces. The positive
        direction of the y-axis is incident on the left face and exits the
        right face. The direction of rotation is defined with respect to
        the positive y-axis.
        """
        assert layer >= 0 and layer < self.N

        if layer == 0:
            left_face = self.faces[FaceEnum.LEFT]
            left_face.rotate_ccw()

        if layer == self.last_layer:
            right_face = self.faces[FaceEnum.RIGHT]
            right_face.rotate_cw()

        up_face = self.faces[FaceEnum.UP]
        up_index = layer
        up_slice = up_face.get_col_slice(up_index)
        up_slice = up_slice.rotate_ht()

        back_face = self.faces[FaceEnum.BACK]
        back_index = self.last_layer - layer
        back_slice = back_face.get_col_slice(back_index)
        back_slice = back_slice.rotate_ht()

        down_face = self.faces[FaceEnum.DOWN]
        down_index = layer
        down_slice = down_face.get_col_slice(down_index)

        front_face = self.faces[FaceEnum.FRONT]
        front_index = layer
        front_slice = front_face.get_col_slice(front_index)

        up_face.apply_slice(front_slice, up_index)
        back_face.apply_slice(up_slice, back_index)
        down_face.apply_slice(back_slice, down_index)
        front_face.apply_slice(down_slice, front_index)

    def _ht_rotation_y(self, layer):
        """Does a half-turn rotation of a given layer in the y-axis.

        The y-axis is orthogonal to the front and back faces. The positive
        direction of the y-axis is incident on the left face and exits the
        right face. The direction of rotation is defined with respect to
        the positive y-axis.
        """
        assert layer >= 0 and layer < self.N

        if layer == 0:
            left_face = self.faces[FaceEnum.LEFT]
            left_face.rotate_ht()

        if layer == self.last_layer:
            right_face = self.faces[FaceEnum.RIGHT]
            right_face.rotate_ht()

        up_face = self.faces[FaceEnum.UP]
        up_index = layer
        up_slice = up_face.get_col_slice(up_index)

        back_face = self.faces[FaceEnum.BACK]
        back_index = self.last_layer - layer
        back_slice = back_face.get_col_slice(back_index)
        back_slice = back_slice.rotate_ht()

        down_face = self.faces[FaceEnum.DOWN]
        down_index = layer
        down_slice = down_face.get_col_slice(down_index)

        front_face = self.faces[FaceEnum.FRONT]
        front_index = layer
        front_slice = front_face.get_col_slice(front_index)
        front_slice = front_slice.rotate_ht()

        up_face.apply_slice(down_slice, up_index)
        back_face.apply_slice(front_slice, back_index)
        down_face.apply_slice(up_slice, down_index)
        front_face.apply_slice(back_slice, front_index)

    def _cw_rotation_z(self, layer):
        """Does a clockwise rotation of a given layer in the z-axis.

        The z-axis is orthogonal to the up and down faces. The positive
        direction of the z-axis is incident on the down face and exits the
        up face. The direction of rotation is defined with respect to
        the positive z-axis.
        """
        assert layer >= 0 and layer < self.N

        if layer == 0:
            down_face = self.faces[FaceEnum.DOWN]
            down_face.rotate_cw()

        if layer == self.last_layer:
            up_face = self.faces[FaceEnum.UP]
            up_face.rotate_ccw()

        right_face = self.faces[FaceEnum.RIGHT]
        right_index = self.last_layer - layer
        right_slice = right_face.get_row_slice(right_index)

        back_face = self.faces[FaceEnum.BACK]
        back_index = self.last_layer - layer
        back_slice = back_face.get_row_slice(back_index)

        left_face = self.faces[FaceEnum.LEFT]
        left_index = self.last_layer - layer
        left_slice = left_face.get_row_slice(left_index)

        front_face = self.faces[FaceEnum.FRONT]
        front_index = self.last_layer - layer
        front_slice = front_face.get_row_slice(front_index)

        right_face.apply_slice(front_slice, right_index)
        back_face.apply_slice(right_slice, back_index)
        left_face.apply_slice(back_slice, left_index)
        front_face.apply_slice(left_slice, front_index)

    def _ccw_rotation_z(self, layer):
        """Does a counter-clockwise rotation of a given layer in the z-axis.

        The z-axis is orthogonal to the up and down faces. The positive
        direction of the z-axis is incident on the down face and exits the
        up face. The direction of rotation is defined with respect to
        the positive z-axis.
        """
        assert layer >= 0 and layer < self.N

        if layer == 0:
            down_face = self.faces[FaceEnum.DOWN]
            down_face.rotate_ccw()

        if layer == self.last_layer:
            up_face = self.faces[FaceEnum.UP]
            up_face.rotate_cw()

        right_face = self.faces[FaceEnum.RIGHT]
        right_index = self.last_layer - layer
        right_slice = right_face.get_row_slice(right_index)

        back_face = self.faces[FaceEnum.BACK]
        back_index = self.last_layer - layer
        back_slice = back_face.get_row_slice(back_index)

        left_face = self.faces[FaceEnum.LEFT]
        left_index = self.last_layer - layer
        left_slice = left_face.get_row_slice(left_index)

        front_face = self.faces[FaceEnum.FRONT]
        front_index = self.last_layer - layer
        front_slice = front_face.get_row_slice(front_index)

        right_face.apply_slice(back_slice, right_index)
        back_face.apply_slice(left_slice, back_index)
        left_face.apply_slice(front_slice, left_index)
        front_face.apply_slice(right_slice, front_index)

    def _ht_rotation_z(self, layer):
        """Does a half-turn rotation of a given layer in the z-axis.

        The z-axis is orthogonal to the up and down faces. The positive
        direction of the z-axis is incident on the down face and exits the
        up face. The direction of rotation is defined with respect to
        the positive z-axis.
        """
        assert layer >= 0 and layer < self.N

        if layer == 0:
            down_face = self.faces[FaceEnum.DOWN]
            down_face.rotate_ht()

        if layer == self.last_layer:
            up_face = self.faces[FaceEnum.UP]
            up_face.rotate_ht()

        right_face = self.faces[FaceEnum.RIGHT]
        right_index = self.last_layer - layer
        right_slice = right_face.get_row_slice(right_index)

        back_face = self.faces[FaceEnum.BACK]
        back_index = self.last_layer - layer
        back_slice = back_face.get_row_slice(back_index)

        left_face = self.faces[FaceEnum.LEFT]
        left_index = self.last_layer - layer
        left_slice = left_face.get_row_slice(left_index)

        front_face = self.faces[FaceEnum.FRONT]
        front_index = self.last_layer - layer
        front_slice = front_face.get_row_slice(front_index)

        right_face.apply_slice(left_slice, right_index)
        back_face.apply_slice(front_slice, back_index)
        left_face.apply_slice(right_slice, left_index)
        front_face.apply_slice(back_slice, front_index)
