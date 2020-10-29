from ErnosCube.sticker import Sticker
from ErnosCube.face_enum import FaceEnum
from ErnosCube.orient_enum import OrientEnum

from plane_rotatable_tests import PlaneRotatableTests
from strategies import stickers, face_enums, orient_enums
from hypothesis import given
from pytest import mark


class TestSticker(PlaneRotatableTests):
    """Collection of all tests run on instances of the Sticker Class.

    Note that the implementations of `test_rotate_*` are not as
    exhaustive as they are in `test_orient_enum`. This is because if
    the rotation methods are properly defined for `OrientEnum` then
    the rotations for `Sticker` should naturally work.
    """

    objs = stickers
    objs_minus_c2 = stickers
    objs_minus_c4 = stickers

    @mark.dependency(name="construction")
    @given(face_enums, orient_enums)
    def test_construction(self, face_enum, orient_enum):
        Sticker(face_enum, orient_enum)

    @mark.dependency(depends=["construction"])
    def test_rotate_cw(self):
        sticker = Sticker(FaceEnum.FRONT, OrientEnum.UP)
        sticker.rotate_cw()
        assert sticker.init_face_enum == FaceEnum.FRONT
        assert sticker.orient_enum == OrientEnum.RIGHT

    @mark.dependency(depends=["construction"])
    def test_rotate_ccw(self):
        sticker = Sticker(FaceEnum.FRONT, OrientEnum.UP)
        sticker.rotate_ccw()
        assert sticker.init_face_enum == FaceEnum.FRONT
        assert sticker.orient_enum == OrientEnum.LEFT

    @mark.dependency(depends=["construction"])
    def test_rotate_ht(self):
        sticker = Sticker(FaceEnum.FRONT, OrientEnum.UP)
        sticker.rotate_ht()
        assert sticker.init_face_enum == FaceEnum.FRONT
        assert sticker.orient_enum == OrientEnum.DOWN

    @mark.dependency(depends=["construction"])
    @given(face_enums, orient_enums)
    def test_str(self, face_enum, orient_enum):
        sticker = Sticker(face_enum, orient_enum)
        gold = f"Sticker({face_enum}, {orient_enum})"
        assert str(sticker) == gold

    @mark.dependency(depends=["construction"])
    @given(stickers)
    def test_get_raw_repr_size(self, sticker):
        assert sticker.get_raw_repr_size() == 3

    @mark.dependency(depends=["construction"])
    @given(face_enums, orient_enums)
    def test_repr(self, face_enum, orient_enum):
        sticker = Sticker(face_enum, orient_enum)
        sticker_repr = repr(sticker)
        orient_repr = repr(orient_enum)
        assert orient_repr in sticker_repr
