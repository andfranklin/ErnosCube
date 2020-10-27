import pytest
from ErnosCube.face_enum import FaceEnum

class TestFaceEnum:
    def test_get_enum(self):
        assert FaceEnum.get_enum(0) == FaceEnum.get_enum("front")
        assert FaceEnum.get_enum(1) == FaceEnum.get_enum("right")
        assert FaceEnum.get_enum(2) == FaceEnum.get_enum("back")
        assert FaceEnum.get_enum(3) == FaceEnum.get_enum("left")
        assert FaceEnum.get_enum(4) == FaceEnum.get_enum("up")
        assert FaceEnum.get_enum(5) == FaceEnum.get_enum("down")


    def test_get_enum_failure_1(self):
        with pytest.raises(Exception):
            FaceEnum.get_enum(-1)


    def test_get_enum_failure_2(self):
        with pytest.raises(Exception):
            FaceEnum.get_enum("blob")


    def test_items(self):
        assert len(FaceEnum.items()) == 6


    def test_get_int(self):
        for _, enum in FaceEnum.items():
            assert FaceEnum.get_int(enum) == enum.value


    def test_get_str(self):
        for _, enum in FaceEnum.items():
            assert FaceEnum.get_str(enum) == enum.name
