from ErnosCube.cube import Cube
from ErnosCube.face import Face
from ErnosCube.sticker import Sticker
from ErnosCube.face_enum import FaceEnum
from ErnosCube.orient_enum import OrientEnum

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
        faces[FaceEnum.FRONT] = Face(stickers)

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
        faces[FaceEnum.BACK] = Face(stickers)

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
        faces[FaceEnum.LEFT] = Face(stickers)

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
        faces[FaceEnum.RIGHT] = Face(stickers)

        stickers = [
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
        ]
        faces[FaceEnum.UP] = Face(stickers)

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
        faces[FaceEnum.DOWN] = Face(stickers)

        cube = Cube.from_faces(faces)
        assert cube.N == 2
        assert len(cube.faces) == 6
        assert len(cube.stickers) == 24

    @mark.dependency(depends=["construction"])
    @given(cubes)
    def test_get_face(self, cube):
        front_face = cube.get_face("front")
        for row in front_face.stickers:
            assert all(sticker.init_face_enum == FaceEnum.FRONT for sticker in row)

        back_face = cube.get_face(FaceEnum.BACK)
        for row in back_face.stickers:
            assert all(sticker.init_face_enum == FaceEnum.BACK for sticker in row)

    @mark.dependency(depends=["construction"])
    @given(cubes)
    def test_str(self, cube):
        assert str(cube) == f"Cube(N={cube.N})"

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

    @mark.dependency(name="deepcopy", depends=["construction"])
    @given(cubes)
    def test_deepcopy(self, cube):
        cube_copy = deepcopy(cube)
        for face, face_copy in zip(cube.faces.values(), cube_copy.faces.values()):
            stickers = face.stickers
            stickers_copy = face_copy.stickers
            for row, row_copy in zip(stickers, stickers_copy):
                for sticker, sticker_copy in zip(row, row_copy):
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
        faces[FaceEnum.FRONT] = Face(stickers)

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
        faces[FaceEnum.BACK] = Face(stickers)

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
        faces[FaceEnum.LEFT] = Face(stickers)

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
        faces[FaceEnum.RIGHT] = Face(stickers)

        stickers = [
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
            ],
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
        ]
        faces[FaceEnum.UP] = Face(stickers)

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
        faces[FaceEnum.DOWN] = Face(stickers)
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
        faces[FaceEnum.FRONT] = Face(stickers)

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
        faces[FaceEnum.BACK] = Face(stickers)

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
        faces[FaceEnum.LEFT] = Face(stickers)

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
        faces[FaceEnum.RIGHT] = Face(stickers)

        stickers = [
            [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
            [
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
                Sticker(FaceEnum.RIGHT, OrientEnum.LEFT),
            ],
        ]
        faces[FaceEnum.UP] = Face(stickers)

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
        faces[FaceEnum.DOWN] = Face(stickers)
        gold_cube = Cube.from_faces(faces)

        cube_2._cw_rotation_x(1)

        assert cube_2 == gold_cube, f"{cube_2}\n{repr(cube_2)}"

    @mark.dependency(depends=["inequality", "cw_rotation_x_0", "cw_rotation_x_1"])
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

    # @mark.dependency(name="cw_rotation_x_1", depends=["equality", "from_faces"])
    # def test_cw_rotation_x_1(self, cube_2):
    #     faces = {}

    #     stickers = [
    #     [Sticker(FaceEnum.FRONT, OrientEnum.UP), Sticker(FaceEnum.FRONT, OrientEnum.UP)],
    #     [Sticker(FaceEnum.FRONT, OrientEnum.UP), Sticker(FaceEnum.FRONT, OrientEnum.UP)]
    #     ]
    #     faces[FaceEnum.FRONT] = Face(stickers)

    #     stickers = [
    #     [Sticker(FaceEnum.BACK, OrientEnum.UP), Sticker(FaceEnum.BACK, OrientEnum.UP)],
    #     [Sticker(FaceEnum.BACK, OrientEnum.UP), Sticker(FaceEnum.BACK, OrientEnum.UP)]
    #     ]
    #     faces[FaceEnum.BACK] = Face(stickers)

    #     stickers = [
    #     [Sticker(FaceEnum.LEFT, OrientEnum.UP), Sticker(FaceEnum.LEFT, OrientEnum.UP)],
    #     [Sticker(FaceEnum.LEFT, OrientEnum.UP), Sticker(FaceEnum.LEFT, OrientEnum.UP)]
    #     ]
    #     faces[FaceEnum.LEFT] = Face(stickers)

    #     stickers = [
    #     [Sticker(FaceEnum.RIGHT, OrientEnum.UP), Sticker(FaceEnum.RIGHT, OrientEnum.UP)],
    #     [Sticker(FaceEnum.RIGHT, OrientEnum.UP), Sticker(FaceEnum.RIGHT, OrientEnum.UP)]
    #     ]
    #     faces[FaceEnum.RIGHT] = Face(stickers)

    #     stickers = [
    #     [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)],
    #     [Sticker(FaceEnum.UP, OrientEnum.UP), Sticker(FaceEnum.UP, OrientEnum.UP)]
    #     ]
    #     faces[FaceEnum.UP] = Face(stickers)

    #     stickers = [
    #     [Sticker(FaceEnum.DOWN, OrientEnum.UP), Sticker(FaceEnum.DOWN, OrientEnum.UP)],
    #     [Sticker(FaceEnum.DOWN, OrientEnum.UP), Sticker(FaceEnum.DOWN, OrientEnum.UP)]
    #     ]
    #     faces[FaceEnum.DOWN] = Face(stickers)
    #     gold_cube = Cube.from_faces(faces)

    #     cube_2._cw_rotation_x(1)

    #     print()
    #     print(repr(cube_2))
    #     print()

    #     print()
    #     print(repr(gold_cube))
    #     print()

    #     assert cube_2 == gold_cube, f"{cube_2}\n{repr(cube_2)}"
