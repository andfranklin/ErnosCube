from ErnosCube.cube import Cube
from ErnosCube.face_enum import FaceEnum

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
