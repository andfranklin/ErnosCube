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

    def test_get_enum_failure_3(self):
        with pytest.raises(Exception):
            FaceEnum.get_enum(123.456)

    def test_items(self):
        assert len(FaceEnum.items()) == 6

    def test_get_int(self):
        for _, enum in FaceEnum.items():
            assert FaceEnum.get_int(enum) == enum.value

    def test_get_str(self):
        for _, enum in FaceEnum.items():
            assert FaceEnum.get_str(enum) == enum.name

    def is_term_color_correct(self, enum, gold):
        value = enum.get_terminal_color()
        assert isinstance(value, str)
        assert value == gold

    def test_get_terminal_color(self):
        self.is_term_color_correct(FaceEnum.FRONT, "green")
        self.is_term_color_correct(FaceEnum.RIGHT, "red")
        self.is_term_color_correct(FaceEnum.BACK, "yellow")
        self.is_term_color_correct(FaceEnum.LEFT, "magenta")
        self.is_term_color_correct(FaceEnum.UP, "white")
        self.is_term_color_correct(FaceEnum.DOWN, "blue")
