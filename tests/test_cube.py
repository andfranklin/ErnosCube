from ErnosCube.cube import Cube

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
