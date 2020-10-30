from ErnosCube.cube import Cube
from ErnosCube.face_enum import FaceEnum

from strategies import cubes
from hypothesis import given
from pytest import raises, mark


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
