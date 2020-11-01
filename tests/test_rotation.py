from ErnosCube.rotation import AxisEnum, MagEnum, Rotation
from strategies import axis_enums, mag_enums, layers, rotations
from hypothesis import given
from pytest import mark, raises


class TestRotation:
    """Collection of all tests run on instances of Rotation."""

    @mark.dependency(name="construction")
    @given(axis_enums, mag_enums, layers)
    def test_construction(self, axis, mag, layer):
        Rotation(axis, mag, layer)

    @mark.dependency(name="construction_failure", depends=["construction"])
    @given(axis_enums, mag_enums)
    def test_construction_failure(self, axis, mag):
        with raises(AssertionError):
            Rotation(axis, mag, -2)
