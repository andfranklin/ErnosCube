from ErnosCube.cube import Cube
from ErnosCube.face import Face
from ErnosCube.sticker import Sticker
from ErnosCube.face_enum import FaceEnum
from ErnosCube.orient_enum import OrientEnum

from utils import N_and_flatten
from strategies import cubes
from hypothesis import given
from pytest import raises, mark, fixture
from copy import deepcopy


class TestCube:
    """Collection of all tests run on instances of the Cube Class."""

    @mark.dependency(name="construction")
    def test_construction(self):
        Cube(N=1)
        Cube(N=2)
        Cube(N=3)

    def test_construction_failure(self):
        with raises(AssertionError):
            Cube(N=0)

        with raises(AssertionError):
            Cube(N=-1)

    @mark.dependency(name="from_faces", depends=["construction"])
    def test_from_faces(self):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))

        cube = Cube.from_faces(faces)
        assert cube.N == 2
        assert len(cube.faces) == 6
        assert len(cube.stickers) == 24

    @mark.dependency(depends=["construction"])
    @given(cubes)
    def test_get_face(self, cube):
        front_face = cube.get_face("front")
        assert all(
            sticker.init_face_enum == FaceEnum.FRONT for sticker in front_face.stickers
        )

        back_face = cube.get_face(FaceEnum.BACK)
        assert all(
            sticker.init_face_enum == FaceEnum.BACK for sticker in back_face.stickers
        )

    @mark.dependency(depends=["construction"])
    @given(cubes)
    def test_str(self, cube):
        assert str(cube) == f"Cube(N={cube.N})"

    @fixture
    def cube_1(self):
        return Cube(N=1)

    @fixture
    def cube_2(self):
        return Cube(N=2)

    @fixture
    def cube_3(self):
        return Cube(N=3)

    @mark.dependency(depends=["construction"])
    def test_repr(self, cube_3):
        gold = "         \x1b[7m\x1b[1m\x1b[37m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[37m ↑ "
        gold += (
            "\x1b[0m\x1b[7m\x1b[1m\x1b[37m ↑ \x1b[0m\n         \x1b[7m\x1b[1m\x1b[37m"
        )
        gold += " ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[37m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[37m ↑ \x1b[0m\n"
        gold += "         \x1b[7m\x1b[1m\x1b[37m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[37m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[37m ↑ \x1b[0m\n\x1b[7m\x1b[1m\x1b[35m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[35m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[35m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[31m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[31m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[31m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[33m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[33m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[33m ↑ \x1b[0m\n\x1b[7m\x1b[1m\x1b[35m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[35m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[35m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[31m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[31m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[31m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[33m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[33m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[33m ↑ \x1b[0m\n\x1b[7m\x1b[1m\x1b[35m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[35m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[35m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[32m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[31m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[31m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[31m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[33m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[33m ↑ "
        gold += (
            "\x1b[0m\x1b[7m\x1b[1m\x1b[33m ↑ \x1b[0m\n         \x1b[7m\x1b[1m\x1b[34m"
        )
        gold += " ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[34m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[34m ↑ "
        gold += (
            "\x1b[0m\n         \x1b[7m\x1b[1m\x1b[34m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[34m"
        )
        gold += " ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[34m ↑ \x1b[0m\n         "
        gold += "\x1b[7m\x1b[1m\x1b[34m ↑ \x1b[0m\x1b[7m\x1b[1m\x1b[34m ↑ "
        gold += "\x1b[0m\x1b[7m\x1b[1m\x1b[34m ↑ \x1b[0m"
        assert (
            repr(cube_3) == gold
        ), f"{cube_3}:\n{repr(cube_3)}\n\n{repr(repr(cube_3))}"

    @mark.dependency(depends=["construction"])
    def test_get_raw_repr_size(self, cube_3):
        width, height = cube_3.get_raw_repr_size()
        assert width == 36
        assert height == 9

    @mark.dependency(name="deepcopy", depends=["construction"])
    @given(cubes)
    def test_deepcopy(self, cube):
        cube_copy = deepcopy(cube)
        for face, face_copy in zip(cube.faces.values(), cube_copy.faces.values()):
            stickers = face.stickers
            stickers_copy = face_copy.stickers
            for sticker, sticker_copy in zip(stickers, stickers_copy):
                assert sticker == sticker_copy
                assert sticker is not sticker_copy

    @mark.dependency(name="equality", depends=["deepcopy"])
    @given(cubes)
    def test_equality(self, cube):
        assert cube == cube
        cube_copy = deepcopy(cube)
        assert cube is not cube_copy
        assert cube == cube_copy

    @mark.dependency(name="inequality", depends=["equality"])
    @given(cubes, cubes)
    def test_inequality(self, a, b):
        if a == b:
            assert not (a != b)
        else:
            assert a != b

    @mark.dependency(name="cw_rotation_x_0", depends=["equality", "from_faces"])
    def test_cw_rotation_x_0(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.RIGHT),
                Sticker(FaceEnum.BACK, OrientEnum.RIGHT),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.RIGHT),
                Sticker(FaceEnum.BACK, OrientEnum.RIGHT),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.UP, OrientEnum.LEFT),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.UP, OrientEnum.LEFT),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.LEFT),
            ],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.LEFT),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
            ],
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.LEFT),
                Sticker(FaceEnum.LEFT, OrientEnum.LEFT),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        gold_cube = Cube.from_faces(faces)
        cube_2._cw_rotation_x(0)
        assert cube_2 == gold_cube, f"{cube_2}\n{repr(cube_2)}"

    @mark.dependency(name="cw_rotation_x_1", depends=["equality", "from_faces"])
    def test_cw_rotation_x_1(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.LEFT),
                Sticker(FaceEnum.FRONT, OrientEnum.LEFT),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.LEFT),
                Sticker(FaceEnum.FRONT, OrientEnum.LEFT),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.UP, OrientEnum.LEFT),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.UP, OrientEnum.LEFT),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.LEFT),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.LEFT),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
            ],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.LEFT),
                Sticker(FaceEnum.LEFT, OrientEnum.LEFT),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        gold_cube = Cube.from_faces(faces)
        cube_2._cw_rotation_x(1)
        assert cube_2 == gold_cube, f"{cube_2}\n{repr(cube_2)}"

    @mark.dependency(
        name="cw_rotation_x_arbitrary",
        depends=["inequality", "cw_rotation_x_0", "cw_rotation_x_1"],
    )
    @given(cubes)
    def test_cw_rotation_x_arbitrary(self, cube):
        rotated_cubes = []
        for i in range(cube.N):
            cube_copy = deepcopy(cube)
            cube_copy._cw_rotation_x(i)

            err_str = f"{cube}._cw_rotation_x({i}):\n{repr(cube)}\n\n{repr(cube_copy)}"
            assert cube != cube_copy, err_str
            for rotated_cube in rotated_cubes:
                assert cube_copy != rotated_cube, err_str

            rotated_cubes.append(cube_copy)

    @mark.dependency(name="ccw_rotation_x_0", depends=["equality", "from_faces"])
    def test_ccw_rotation_x_0(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.RIGHT),
                Sticker(FaceEnum.BACK, OrientEnum.RIGHT),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.RIGHT),
                Sticker(FaceEnum.BACK, OrientEnum.RIGHT),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.UP, OrientEnum.LEFT),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.UP, OrientEnum.LEFT),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.LEFT),
            ],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.LEFT),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
            ],
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.LEFT),
                Sticker(FaceEnum.LEFT, OrientEnum.LEFT),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        cube = Cube.from_faces(faces)
        cube._ccw_rotation_x(0)
        assert cube == cube_2, f"{cube}\n{repr(cube)}"

    @mark.dependency(name="ccw_rotation_x_1", depends=["equality", "from_faces"])
    def test_ccw_rotation_x_1(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.LEFT),
                Sticker(FaceEnum.FRONT, OrientEnum.LEFT),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.LEFT),
                Sticker(FaceEnum.FRONT, OrientEnum.LEFT),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.UP, OrientEnum.LEFT),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.UP, OrientEnum.LEFT),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.LEFT),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.LEFT),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
            ],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.LEFT),
                Sticker(FaceEnum.LEFT, OrientEnum.LEFT),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        cube = Cube.from_faces(faces)
        cube._ccw_rotation_x(1)
        assert cube_2 == cube, f"{cube}\n{repr(cube)}"

    @mark.dependency(
        name="ccw_rotation_x_arbitrary",
        depends=["inequality", "ccw_rotation_x_0", "ccw_rotation_x_1"],
    )
    @given(cubes)
    def test_ccw_rotation_x_arbitrary(self, cube):
        rotated_cubes = []
        for i in range(cube.N):
            cube_copy = deepcopy(cube)
            cube_copy._ccw_rotation_x(i)

            err_str = f"{cube}._ccw_rotation_x({i}):\n{repr(cube)}\n\n{repr(cube_copy)}"
            assert cube != cube_copy, err_str
            for rotated_cube in rotated_cubes:
                assert cube_copy != rotated_cube, err_str

            rotated_cubes.append(cube_copy)

    @mark.dependency(name="ht_rotation_x_0", depends=["equality", "from_faces"])
    def test_ht_rotation_x_0(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.DOWN),
                Sticker(FaceEnum.BACK, OrientEnum.DOWN),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.DOWN),
                Sticker(FaceEnum.BACK, OrientEnum.DOWN),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.DOWN),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.DOWN),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.DOWN),
            ],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.DOWN),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.DOWN),
                Sticker(FaceEnum.DOWN, OrientEnum.DOWN),
            ],
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.UP, OrientEnum.DOWN),
                Sticker(FaceEnum.UP, OrientEnum.DOWN),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        gold_cube = Cube.from_faces(faces)
        cube_2._ht_rotation_x(0)
        assert cube_2 == gold_cube, f"{cube_2}\n{repr(cube_2)}"

    @mark.dependency(name="ht_rotation_x_1", depends=["equality", "from_faces"])
    def test_ht_rotation_x_1(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.DOWN),
                Sticker(FaceEnum.FRONT, OrientEnum.DOWN),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.DOWN),
                Sticker(FaceEnum.FRONT, OrientEnum.DOWN),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.DOWN),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.DOWN),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.DOWN),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.DOWN),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.DOWN),
                Sticker(FaceEnum.DOWN, OrientEnum.DOWN),
            ],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.UP, OrientEnum.DOWN),
                Sticker(FaceEnum.UP, OrientEnum.DOWN),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        gold_cube = Cube.from_faces(faces)
        cube_2._ht_rotation_x(1)
        assert cube_2 == gold_cube, f"{cube_2}\n{repr(cube_2)}"

    @mark.dependency(
        name="ht_rotation_x_arbitrary",
        depends=["inequality", "ht_rotation_x_0", "ht_rotation_x_1"],
    )
    @given(cubes)
    def test_ht_rotation_x_arbitrary(self, cube):
        rotated_cubes = []
        for i in range(cube.N):
            cube_copy = deepcopy(cube)
            cube_copy._ht_rotation_x(i)

            err_str = f"{cube}._ht_rotation_x({i}):\n{repr(cube)}\n\n{repr(cube_copy)}"
            assert cube != cube_copy, err_str
            for rotated_cube in rotated_cubes:
                assert cube_copy != rotated_cube, err_str

            rotated_cubes.append(cube_copy)

    @mark.dependency(name="cw_rotation_y_0", depends=["equality", "from_faces"])
    def test_cw_rotation_y_0(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.UP, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.UP, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.DOWN),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.DOWN),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.RIGHT),
                Sticker(FaceEnum.LEFT, OrientEnum.RIGHT),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.RIGHT),
                Sticker(FaceEnum.LEFT, OrientEnum.RIGHT),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.DOWN),
                Sticker(FaceEnum.UP, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.DOWN),
                Sticker(FaceEnum.UP, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        gold_cube = Cube.from_faces(faces)
        cube_2._cw_rotation_y(0)
        assert cube_2 == gold_cube, f"{cube_2}\n{repr(cube_2)}"

    @mark.dependency(name="cw_rotation_y_1", depends=["equality", "from_faces"])
    def test_cw_rotation_y_1(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.UP, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.UP, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.DOWN),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.DOWN),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
            ],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.UP, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.DOWN),
            ],
            [
                Sticker(FaceEnum.UP, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.DOWN),
            ],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        gold_cube = Cube.from_faces(faces)
        cube_2._cw_rotation_y(1)
        assert cube_2 == gold_cube, f"{cube_2}\n{repr(cube_2)}"

    @mark.dependency(
        name="cw_rotation_y_arbitrary",
        depends=["inequality", "cw_rotation_y_0", "cw_rotation_y_1"],
    )
    @given(cubes)
    def test_cw_rotation_y_arbitrary(self, cube):
        rotated_cubes = []
        for i in range(cube.N):
            cube_copy = deepcopy(cube)
            cube_copy._cw_rotation_y(i)

            err_str = f"{cube}._cw_rotation_y({i}):\n{repr(cube)}\n\n{repr(cube_copy)}"
            assert cube != cube_copy, err_str
            for rotated_cube in rotated_cubes:
                assert cube_copy != rotated_cube, err_str

            rotated_cubes.append(cube_copy)

    @mark.dependency(name="ccw_rotation_y_0", depends=["equality", "from_faces"])
    def test_ccw_rotation_y_0(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.UP, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.UP, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.DOWN),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.DOWN),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.RIGHT),
                Sticker(FaceEnum.LEFT, OrientEnum.RIGHT),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.RIGHT),
                Sticker(FaceEnum.LEFT, OrientEnum.RIGHT),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.DOWN),
                Sticker(FaceEnum.UP, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.DOWN),
                Sticker(FaceEnum.UP, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        cube = Cube.from_faces(faces)
        cube._ccw_rotation_y(0)
        assert cube_2 == cube, f"{cube}\n{repr(cube)}"

    @mark.dependency(name="ccw_rotation_y_1", depends=["equality", "from_faces"])
    def test_ccw_rotation_y_1(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.UP, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.UP, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.DOWN),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.DOWN),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
            ],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.UP, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.DOWN),
            ],
            [
                Sticker(FaceEnum.UP, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.DOWN),
            ],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        cube = Cube.from_faces(faces)
        cube._ccw_rotation_y(1)
        assert cube_2 == cube, f"{cube}\n{repr(cube)}"

    @mark.dependency(
        name="ccw_rotation_y_arbitrary",
        depends=["inequality", "ccw_rotation_y_0", "ccw_rotation_y_1"],
    )
    @given(cubes)
    def test_ccw_rotation_y_arbitrary(self, cube):
        rotated_cubes = []
        for i in range(cube.N):
            cube_copy = deepcopy(cube)
            cube_copy._ccw_rotation_y(i)

            err_str = f"{cube}._ccw_rotation_y({i}):\n{repr(cube)}\n\n{repr(cube_copy)}"
            assert cube != cube_copy, err_str
            for rotated_cube in rotated_cubes:
                assert cube_copy != rotated_cube, err_str

            rotated_cubes.append(cube_copy)

    @mark.dependency(name="ht_rotation_y_0", depends=["equality", "from_faces"])
    def test_ht_rotation_y_0(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.DOWN),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.DOWN),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.DOWN),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.DOWN),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.DOWN),
                Sticker(FaceEnum.LEFT, OrientEnum.DOWN),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.DOWN),
                Sticker(FaceEnum.LEFT, OrientEnum.DOWN),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.UP, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.UP, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.UP, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.UP, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        gold_cube = Cube.from_faces(faces)
        cube_2._ht_rotation_y(0)
        assert cube_2 == gold_cube, f"{cube_2}\n{repr(cube_2)}"

    @mark.dependency(name="ht_rotation_y_1", depends=["equality", "from_faces"])
    def test_ht_rotation_y_1(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.DOWN),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.DOWN),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.DOWN),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.DOWN),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.DOWN),
                Sticker(FaceEnum.RIGHT, OrientEnum.DOWN),
            ],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.DOWN),
                Sticker(FaceEnum.RIGHT, OrientEnum.DOWN),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.UP, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.UP, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.UP, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.UP, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        gold_cube = Cube.from_faces(faces)
        cube_2._ht_rotation_y(1)
        assert cube_2 == gold_cube, f"{cube_2}\n{repr(cube_2)}"

    @mark.dependency(
        name="ht_rotation_y_arbitrary",
        depends=["inequality", "ht_rotation_y_0", "ht_rotation_y_1"],
    )
    @given(cubes)
    def test_ht_rotation_y_arbitrary(self, cube):
        rotated_cubes = []
        for i in range(cube.N):
            cube_copy = deepcopy(cube)
            cube_copy._ht_rotation_y(i)

            err_str = f"{cube}._ht_rotation_y({i}):\n{repr(cube)}\n\n{repr(cube_copy)}"
            assert cube != cube_copy, err_str
            for rotated_cube in rotated_cubes:
                assert cube_copy != rotated_cube, err_str

            rotated_cubes.append(cube_copy)

    @mark.dependency(name="cw_rotation_z_0", depends=["equality", "from_faces"])
    def test_cw_rotation_z_0(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.RIGHT),
                Sticker(FaceEnum.DOWN, OrientEnum.RIGHT),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.RIGHT),
                Sticker(FaceEnum.DOWN, OrientEnum.RIGHT),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        gold_cube = Cube.from_faces(faces)
        cube_2._cw_rotation_z(0)
        assert cube_2 == gold_cube, f"{cube_2}\n{repr(cube_2)}"

    @mark.dependency(name="cw_rotation_z_1", depends=["equality", "from_faces"])
    def test_cw_rotation_z_1(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.UP, OrientEnum.LEFT),
                Sticker(FaceEnum.UP, OrientEnum.LEFT),
            ],
            [
                Sticker(FaceEnum.UP, OrientEnum.LEFT),
                Sticker(FaceEnum.UP, OrientEnum.LEFT),
            ],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        gold_cube = Cube.from_faces(faces)
        cube_2._cw_rotation_z(1)
        assert cube_2 == gold_cube, f"{cube_2}\n{repr(cube_2)}"

    @mark.dependency(
        name="cw_rotation_z_arbitrary",
        depends=["inequality", "cw_rotation_z_0", "cw_rotation_z_1"],
    )
    @given(cubes)
    def test_cw_rotation_z_arbitrary(self, cube):
        rotated_cubes = []
        for i in range(cube.N):
            cube_copy = deepcopy(cube)
            cube_copy._cw_rotation_z(i)

            err_str = f"{cube}._cw_rotation_z({i}):\n{repr(cube)}\n\n{repr(cube_copy)}"
            assert cube != cube_copy, err_str
            for rotated_cube in rotated_cubes:
                assert cube_copy != rotated_cube, err_str

            rotated_cubes.append(cube_copy)

    @mark.dependency(name="ccw_rotation_z_0", depends=["equality", "from_faces"])
    def test_ccw_rotation_z_0(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.RIGHT),
                Sticker(FaceEnum.DOWN, OrientEnum.RIGHT),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.RIGHT),
                Sticker(FaceEnum.DOWN, OrientEnum.RIGHT),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        cube = Cube.from_faces(faces)
        cube._ccw_rotation_z(0)
        assert cube_2 == cube, f"{cube}\n{repr(cube)}"

    @mark.dependency(name="ccw_rotation_z_1", depends=["equality", "from_faces"])
    def test_ccw_rotation_z_1(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.UP, OrientEnum.LEFT),
                Sticker(FaceEnum.UP, OrientEnum.LEFT),
            ],
            [
                Sticker(FaceEnum.UP, OrientEnum.LEFT),
                Sticker(FaceEnum.UP, OrientEnum.LEFT),
            ],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        cube = Cube.from_faces(faces)
        cube._ccw_rotation_z(1)
        assert cube_2 == cube, f"{cube}\n{repr(cube)}"

    @mark.dependency(
        name="ccw_rotation_z_arbitrary",
        depends=["inequality", "ccw_rotation_z_0", "ccw_rotation_z_1"],
    )
    @given(cubes)
    def test_ccw_rotation_z_arbitrary(self, cube):
        rotated_cubes = []
        for i in range(cube.N):
            cube_copy = deepcopy(cube)
            cube_copy._ccw_rotation_z(i)

            err_str = f"{cube}._ccw_rotation_z({i}):\n{repr(cube)}\n\n{repr(cube_copy)}"
            assert cube != cube_copy, err_str
            for rotated_cube in rotated_cubes:
                assert cube_copy != rotated_cube, err_str

            rotated_cubes.append(cube_copy)

    @mark.dependency(name="ht_rotation_z_0", depends=["equality", "from_faces"])
    def test_ht_rotation_z_0(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.DOWN),
                Sticker(FaceEnum.DOWN, OrientEnum.DOWN),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.DOWN),
                Sticker(FaceEnum.DOWN, OrientEnum.DOWN),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        cube = Cube.from_faces(faces)
        cube_2._ht_rotation_z(0)
        assert cube_2 == cube, f"{cube}\n{repr(cube)}"

    @mark.dependency(name="ht_rotation_z_1", depends=["equality", "from_faces"])
    def test_ht_rotation_z_1(self, cube_2):
        faces = {}

        stickers = [
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.FRONT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
                Sticker(FaceEnum.FRONT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.BACK, OrientEnum.UP),
                Sticker(FaceEnum.BACK, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.BACK] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.LEFT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
                Sticker(FaceEnum.LEFT, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
                Sticker(FaceEnum.RIGHT, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.RIGHT] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.UP, OrientEnum.DOWN),
                Sticker(FaceEnum.UP, OrientEnum.DOWN),
            ],
            [
                Sticker(FaceEnum.UP, OrientEnum.DOWN),
                Sticker(FaceEnum.UP, OrientEnum.DOWN),
            ],
        ]
        faces[FaceEnum.UP] = Face(*N_and_flatten(stickers))

        stickers = [
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
            [
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
                Sticker(FaceEnum.DOWN, OrientEnum.UP),
            ],
        ]
        faces[FaceEnum.DOWN] = Face(*N_and_flatten(stickers))
        cube = Cube.from_faces(faces)
        cube_2._ht_rotation_z(1)
        assert cube_2 == cube, f"{cube}\n{repr(cube)}"

    @mark.dependency(
        name="ht_rotation_z_arbitrary",
        depends=["inequality", "ht_rotation_z_0", "ht_rotation_z_1"],
    )
    @given(cubes)
    def test_ht_rotation_z_arbitrary(self, cube):
        rotated_cubes = []
        for i in range(cube.N):
            cube_copy = deepcopy(cube)
            cube_copy._ht_rotation_z(i)

            err_str = f"{cube}._ht_rotation_z({i}):\n{repr(cube)}\n\n{repr(cube_copy)}"
            assert cube != cube_copy, err_str
            for rotated_cube in rotated_cubes:
                assert cube_copy != rotated_cube, err_str

            rotated_cubes.append(cube_copy)

    @mark.dependency(name="cw_rotation_x", depends=["equality", "from_faces"])
    def test_cw_rotation_x(self, cube_1):
        faces = {}

        stickers = [Sticker(FaceEnum.FRONT, OrientEnum.LEFT)]
        faces[FaceEnum.FRONT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.BACK, OrientEnum.RIGHT)]
        faces[FaceEnum.BACK] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.UP, OrientEnum.LEFT)]
        faces[FaceEnum.LEFT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.DOWN, OrientEnum.LEFT)]
        faces[FaceEnum.RIGHT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.RIGHT, OrientEnum.LEFT)]
        faces[FaceEnum.UP] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.LEFT, OrientEnum.LEFT)]
        faces[FaceEnum.DOWN] = Face(1, stickers)

        gold_cube = Cube.from_faces(faces)
        cube_1._cw_all_rotation_x()
        assert cube_1 == gold_cube, f"{cube_1}\n{repr(cube_1)}"

    @mark.dependency(depends=["cw_rotation_x_arbitrary", "cw_rotation_x"])
    @given(cubes)
    def test_cw_rotation_x_equiv(self, cube):
        cube_copy = deepcopy(cube)
        for i in range(cube.N):
            cube_copy._cw_rotation_x(i)
        cube._cw_all_rotation_x()
        assert cube == cube_copy, f"{cube}: {repr(cube)}"

    @mark.dependency(name="ccw_rotation_x", depends=["equality", "from_faces"])
    def test_ccw_rotation_x(self, cube_1):
        faces = {}

        stickers = [Sticker(FaceEnum.FRONT, OrientEnum.RIGHT)]
        faces[FaceEnum.FRONT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.BACK, OrientEnum.LEFT)]
        faces[FaceEnum.BACK] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.DOWN, OrientEnum.RIGHT)]
        faces[FaceEnum.LEFT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.UP, OrientEnum.RIGHT)]
        faces[FaceEnum.RIGHT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.LEFT, OrientEnum.RIGHT)]
        faces[FaceEnum.UP] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.RIGHT, OrientEnum.RIGHT)]
        faces[FaceEnum.DOWN] = Face(1, stickers)

        gold_cube = Cube.from_faces(faces)
        cube_1._ccw_all_rotation_x()
        assert cube_1 == gold_cube, f"{cube_1}\n{repr(cube_1)}"

    @mark.dependency(depends=["ccw_rotation_x_arbitrary", "ccw_rotation_x"])
    @given(cubes)
    def test_ccw_rotation_x_equiv(self, cube):
        cube_copy = deepcopy(cube)
        for i in range(cube.N):
            cube_copy._ccw_rotation_x(i)
        cube._ccw_all_rotation_x()
        assert cube == cube_copy, f"{cube}: {repr(cube)}"

    @mark.dependency(name="ht_rotation_x", depends=["equality", "from_faces"])
    def test_ht_rotation_x(self, cube_1):
        faces = {}

        stickers = [Sticker(FaceEnum.FRONT, OrientEnum.DOWN)]
        faces[FaceEnum.FRONT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.BACK, OrientEnum.DOWN)]
        faces[FaceEnum.BACK] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.RIGHT, OrientEnum.DOWN)]
        faces[FaceEnum.LEFT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.LEFT, OrientEnum.DOWN)]
        faces[FaceEnum.RIGHT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.DOWN, OrientEnum.DOWN)]
        faces[FaceEnum.UP] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.UP, OrientEnum.DOWN)]
        faces[FaceEnum.DOWN] = Face(1, stickers)

        gold_cube = Cube.from_faces(faces)
        cube_1._ht_all_rotation_x()
        assert cube_1 == gold_cube, f"{cube_1}\n{repr(cube_1)}"

    @mark.dependency(depends=["ht_rotation_x_arbitrary", "ht_rotation_x"])
    @given(cubes)
    def test_ht_rotation_x_equiv(self, cube):
        cube_copy = deepcopy(cube)
        for i in range(cube.N):
            cube_copy._ht_rotation_x(i)
        cube._ht_all_rotation_x()
        assert cube == cube_copy, f"{cube}: {repr(cube)}"

    @mark.dependency(name="cw_rotation_y", depends=["equality", "from_faces"])
    def test_cw_rotation_y(self, cube_1):
        faces = {}

        stickers = [Sticker(FaceEnum.UP, OrientEnum.UP)]
        faces[FaceEnum.FRONT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.DOWN, OrientEnum.DOWN)]
        faces[FaceEnum.BACK] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.LEFT, OrientEnum.RIGHT)]
        faces[FaceEnum.LEFT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.RIGHT, OrientEnum.LEFT)]
        faces[FaceEnum.RIGHT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.BACK, OrientEnum.DOWN)]
        faces[FaceEnum.UP] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.FRONT, OrientEnum.UP)]
        faces[FaceEnum.DOWN] = Face(1, stickers)

        gold_cube = Cube.from_faces(faces)
        cube_1._cw_all_rotation_y()
        assert cube_1 == gold_cube, f"{cube_1}\n{repr(cube_1)}"

    @mark.dependency(depends=["cw_rotation_y_arbitrary", "cw_rotation_y"])
    @given(cubes)
    def test_cw_rotation_y_equiv(self, cube):
        cube_copy = deepcopy(cube)
        for i in range(cube.N):
            cube_copy._cw_rotation_y(i)
        cube._cw_all_rotation_y()
        assert cube == cube_copy, f"{cube}: {repr(cube)}"

    @mark.dependency(name="ccw_rotation_y", depends=["equality", "from_faces"])
    def test_ccw_rotation_y(self, cube_1):
        faces = {}

        stickers = [Sticker(FaceEnum.DOWN, OrientEnum.UP)]
        faces[FaceEnum.FRONT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.UP, OrientEnum.DOWN)]
        faces[FaceEnum.BACK] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.LEFT, OrientEnum.LEFT)]
        faces[FaceEnum.LEFT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.RIGHT, OrientEnum.RIGHT)]
        faces[FaceEnum.RIGHT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.FRONT, OrientEnum.UP)]
        faces[FaceEnum.UP] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.BACK, OrientEnum.DOWN)]
        faces[FaceEnum.DOWN] = Face(1, stickers)

        gold_cube = Cube.from_faces(faces)
        cube_1._ccw_all_rotation_y()
        assert cube_1 == gold_cube, f"{cube_1}\n{repr(cube_1)}"

    @mark.dependency(depends=["ccw_rotation_y_arbitrary", "ccw_rotation_y"])
    @given(cubes)
    def test_ccw_rotation_y_equiv(self, cube):
        cube_copy = deepcopy(cube)
        for i in range(cube.N):
            cube_copy._ccw_rotation_y(i)
        cube._ccw_all_rotation_y()
        assert cube == cube_copy, f"{cube}: {repr(cube)}"

    @mark.dependency(name="ht_rotation_y", depends=["equality", "from_faces"])
    def test_ht_rotation_y(self, cube_1):
        faces = {}

        stickers = [Sticker(FaceEnum.BACK, OrientEnum.DOWN)]
        faces[FaceEnum.FRONT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.FRONT, OrientEnum.DOWN)]
        faces[FaceEnum.BACK] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.LEFT, OrientEnum.DOWN)]
        faces[FaceEnum.LEFT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.RIGHT, OrientEnum.DOWN)]
        faces[FaceEnum.RIGHT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.DOWN, OrientEnum.UP)]
        faces[FaceEnum.UP] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.UP, OrientEnum.UP)]
        faces[FaceEnum.DOWN] = Face(1, stickers)

        gold_cube = Cube.from_faces(faces)
        cube_1._ht_all_rotation_y()
        assert cube_1 == gold_cube, f"{cube_1}\n{repr(cube_1)}"

    @mark.dependency(depends=["ht_rotation_y_arbitrary", "ht_rotation_y"])
    @given(cubes)
    def test_ht_rotation_y_equiv(self, cube):
        cube_copy = deepcopy(cube)
        for i in range(cube.N):
            cube_copy._ht_rotation_y(i)
        cube._ht_all_rotation_y()
        assert cube == cube_copy, f"{cube}: {repr(cube)}"

    @mark.dependency(name="cw_rotation_z", depends=["equality", "from_faces"])
    def test_cw_rotation_z(self, cube_1):
        faces = {}

        stickers = [Sticker(FaceEnum.LEFT, OrientEnum.UP)]
        faces[FaceEnum.FRONT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.RIGHT, OrientEnum.UP)]
        faces[FaceEnum.BACK] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.BACK, OrientEnum.UP)]
        faces[FaceEnum.LEFT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.FRONT, OrientEnum.UP)]
        faces[FaceEnum.RIGHT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.UP, OrientEnum.LEFT)]
        faces[FaceEnum.UP] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.DOWN, OrientEnum.RIGHT)]
        faces[FaceEnum.DOWN] = Face(1, stickers)

        gold_cube = Cube.from_faces(faces)
        cube_1._cw_all_rotation_z()
        assert cube_1 == gold_cube, f"{cube_1}\n{repr(cube_1)}"

    @mark.dependency(depends=["cw_rotation_z_arbitrary", "cw_rotation_z"])
    @given(cubes)
    def test_cw_rotation_z_equiv(self, cube):
        cube_copy = deepcopy(cube)
        for i in range(cube.N):
            cube_copy._cw_rotation_z(i)
        cube._cw_all_rotation_z()
        assert cube == cube_copy, f"{cube}: {repr(cube)}"

    @mark.dependency(name="ccw_rotation_z", depends=["equality", "from_faces"])
    def test_ccw_rotation_z(self, cube_1):
        faces = {}

        stickers = [Sticker(FaceEnum.RIGHT, OrientEnum.UP)]
        faces[FaceEnum.FRONT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.LEFT, OrientEnum.UP)]
        faces[FaceEnum.BACK] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.FRONT, OrientEnum.UP)]
        faces[FaceEnum.LEFT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.BACK, OrientEnum.UP)]
        faces[FaceEnum.RIGHT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.UP, OrientEnum.RIGHT)]
        faces[FaceEnum.UP] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.DOWN, OrientEnum.LEFT)]
        faces[FaceEnum.DOWN] = Face(1, stickers)

        gold_cube = Cube.from_faces(faces)
        cube_1._ccw_all_rotation_z()
        assert cube_1 == gold_cube, f"{cube_1}\n{repr(cube_1)}"

    @mark.dependency(depends=["ccw_rotation_z_arbitrary", "ccw_rotation_z"])
    @given(cubes)
    def test_ccw_rotation_z_equiv(self, cube):
        cube_copy = deepcopy(cube)
        for i in range(cube.N):
            cube_copy._ccw_rotation_z(i)
        cube._ccw_all_rotation_z()
        assert cube == cube_copy, f"{cube}: {repr(cube)}"

    @mark.dependency(name="ht_rotation_z", depends=["equality", "from_faces"])
    def test_ht_rotation_z(self, cube_1):
        faces = {}

        stickers = [Sticker(FaceEnum.BACK, OrientEnum.UP)]
        faces[FaceEnum.FRONT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.FRONT, OrientEnum.UP)]
        faces[FaceEnum.BACK] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.RIGHT, OrientEnum.UP)]
        faces[FaceEnum.LEFT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.LEFT, OrientEnum.UP)]
        faces[FaceEnum.RIGHT] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.UP, OrientEnum.DOWN)]
        faces[FaceEnum.UP] = Face(1, stickers)

        stickers = [Sticker(FaceEnum.DOWN, OrientEnum.DOWN)]
        faces[FaceEnum.DOWN] = Face(1, stickers)

        gold_cube = Cube.from_faces(faces)
        cube_1._ht_all_rotation_z()
        assert cube_1 == gold_cube, f"{cube_1}\n{repr(cube_1)}"

    @mark.dependency(depends=["ht_rotation_z_arbitrary", "ht_rotation_z"])
    @given(cubes)
    def test_ht_rotation_z_equiv(self, cube):
        cube_copy = deepcopy(cube)
        for i in range(cube.N):
            cube_copy._ht_rotation_z(i)
        cube._ht_all_rotation_z()
        assert cube == cube_copy, f"{cube}: {repr(cube)}"
