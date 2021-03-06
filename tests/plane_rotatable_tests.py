from ErnosCube.rotation_enum import RotationEnum
from hypothesis import given
from hypothesis.strategies import data
from copy import deepcopy
from pytest import mark, raises


class PlaneRotatableTests:
    """A test suite of tests for classes that inherit `PlaneRotatable`.

    This class implements a suite of propery based tests that all
    `PlaneRotatable` objects are expected to pass. A test suite for a specific
    rotatable class can incorporate this tests by inheriting this class and
    specifying the member variable `objs`, `objs_minus_c4`, and `objs_minus_c2`
    with hypothesis strategies, and implementing the methods
    `construction_test`, `rotate_cw_test`, `rotate_ccw_test`, and
    `rotate_ht_test`.

    The design is such that once each of the rotation methods are sufficiently
    tested for some ground case(s) in `rotate_*_test`, then the property based
    tests implemented with hypothesis will provide additional confidence about
    the correctness of the `rotate_*` methods. It is recognized that
    exhaustively testing the object space of a `PlaneRotatable` class is not
    desirable, or practical. The implementations of each `rotate_*_test` should
    be as straightforward and hard coded as possible. Only a few example cases
    are recommended (although, one could implement an exhaustive test suite in
    this method, if desired). This class makes it sufficient to have only a
    few, hand-selected examples tested so that one can have confidence that the
    methods `rotate_*` are working properly.

    Hypothesis does the heavy lifting by sampling the object space, and
    revealing any unexpected behavior that is encountered. For more information
    about hypothesis see:
    https://hypothesis.readthedocs.io/en/latest/index.html

    The strategy for `objs` should cover as much of object space for the
    `PlaneRotatable` class as practical. This will ensure a wide test coverage
    and increase the chance of an obscure bug being caught.

    The strategy for `objs_minus_c4` should produce arbitrary rotatable objects
    that are not in the `C_4` group. In other words, the generated rotatable
    objects from this strategy should not have 90-degree rotational symmetry.
    Similarly, `objs_minus_c2` should produce rotatable objects that are not in
    the `C_2` group (i.e. they do not have 180-degree symmetry).
    See: https://en.wikipedia.org/wiki/Rotational_symmetry#Discrete_rotational_symmetry

    Neither of the `objs_minus_*` strategies should use the `rotate_*` methods
    in their definition. The intent of these strategies is to test the
    properies of the `rotate_*` methods. If one uses `rotate_*` in the
    definition of a strategy it might lead to a false sense of assurance in the
    correctness of each method's implementations. Since `C_2` is a superset of
    `C_4`, `objs_minus_c2` may be used to generate `objs_minus_c4` using the
    `one_of` strategy from hypothesis. E.g. create `objs_minus_c2` and
    `c2_minus_c4`. Then, `objs_minus_c4 = one_of(objs_minus_c2, c2_minus_c4)`.

    It is anticipated that the specification of the `rotatable_objs_minus_*`
    strategies might be tedious without the use of the `rotate_*` functions.
    So, it is recommended that a subset of the many possible rotatable objects
    are hard coded into the strategy definitions.
    """

    objs = None
    objs_minus_c2 = None
    objs_minus_c4 = None

    @mark.dependency(name="construction")
    def test_construction(self):
        self.construction_test()

    def construction_test(self):
        assert False, "not implemented"

    @mark.dependency(name="rotate_cw", depends=["construction"])
    def test_rotate_cw(self):
        self.rotate_cw_test()

    def rotate_cw_test(self):
        assert False, "not implemented"

    @mark.dependency(name="rotate_ccw", depends=["construction"])
    def test_rotate_ccw(self):
        self.rotate_ccw_test()

    def rotate_ccw_test(self):
        assert False, "not implemented"

    @mark.dependency(name="rotate_ht", depends=["construction"])
    def test_rotate_ht(self):
        self.rotate_ht_test()

    def rotate_ht_test(self):
        assert False, "not implemented"

    @mark.dependency(name="objs")
    def test_objs_def(self):
        assert self.objs is not None

    @mark.dependency(name="objs_minus_c2")
    def test_objs_minus_c2(self):
        assert self.objs_minus_c2 is not None

    @mark.dependency(name="objs_minus_c4")
    def test_objs_minus_c4(self):
        assert self.objs_minus_c4 is not None

    @mark.dependency(name="deepcopy", depends=["construction", "objs"])
    @given(data())
    def test_deepcopy(self, data):
        obj = data.draw(self.objs)
        deepcopy(obj)

    @mark.dependency(name="equality", depends=["deepcopy"])
    @given(data())
    def test_equality(self, data):
        obj = data.draw(self.objs)
        assert obj == obj, f"failed for {str(obj)}\n{repr(obj)}"
        obj_copy = deepcopy(obj)
        assert obj == obj_copy, f"failed for {str(obj)}\n{repr(obj)}"

    @mark.dependency(name="inequality", depends=["equality"])
    @given(data())
    def test_inequality(self, data):
        a = data.draw(self.objs)
        b = data.draw(self.objs)
        if a == b:
            assert (
                not a != b
            ), f"failed for {str(a)}\n{repr(a)}\nand {str(b)}\n{repr(b)}"
        else:
            assert a != b, f"failed for {str(a)}\n{repr(a)}\nand {str(b)}\n{repr(b)}"

    @mark.dependency(depends=["equality", "rotate_cw"])
    @given(data())
    def test_cw_invertability(self, data):
        obj = data.draw(self.objs)
        gold = deepcopy(obj)
        obj = obj.rotate_cw().rotate_cw().rotate_cw().rotate_cw()
        assert obj == gold, f"failed for {str(obj)}\n{repr(obj)}"

    @mark.dependency(depends=["equality", "rotate_ccw"])
    @given(data())
    def test_ccw_invertability(self, data):
        obj = data.draw(self.objs)
        gold = deepcopy(obj)
        obj = obj.rotate_ccw().rotate_ccw().rotate_ccw().rotate_ccw()
        assert obj == gold, f"failed for {str(obj)}\n{repr(obj)}"

    @mark.dependency(depends=["equality", "rotate_ht"])
    @given(data())
    def test_ht_invertability(self, data):
        obj = data.draw(self.objs)
        gold = deepcopy(obj)
        assert (
            obj.rotate_ht().rotate_ht() == gold
        ), f"failed for {str(obj)}\n{repr(obj)}"

    @mark.dependency(depends=["equality", "rotate_cw", "rotate_ccw"])
    @given(data())
    def test_cw_ccw_invertability(self, data):
        obj = data.draw(self.objs)
        gold = deepcopy(obj)
        assert (
            obj.rotate_cw().rotate_ccw() == gold
        ), f"failed for {str(obj)}\n{repr(obj)}"
        assert (
            obj.rotate_ccw().rotate_cw() == gold
        ), f"failed for {str(obj)}\n{repr(obj)}"

    @mark.dependency(depends=["equality", "rotate_cw", "rotate_ht"])
    @given(data())
    def test_ht_2cw_equivalence(self, data):
        obj = data.draw(self.objs)
        gold = deepcopy(obj).rotate_cw().rotate_cw()
        obj = obj.rotate_ht()
        assert obj == gold, f"failed for {str(obj)}\n{repr(obj)}"

    @mark.dependency(depends=["equality", "rotate_ccw", "rotate_ht"])
    @given(data())
    def test_ht_2ccw_equivalence(self, data):
        obj = data.draw(self.objs)
        gold = deepcopy(obj).rotate_ccw().rotate_ccw()
        obj = obj.rotate_ht()
        assert obj == gold, f"failed for {str(obj)}\n{repr(obj)}"

    @mark.dependency(depends=["equality", "rotate_cw", "rotate_ccw"])
    @given(data())
    def test_3cw_ccw_equivalence(self, data):
        obj = data.draw(self.objs)
        gold = deepcopy(obj).rotate_ccw()
        obj = obj.rotate_cw().rotate_cw().rotate_cw()
        assert obj == gold, f"failed for {str(obj)}\n{repr(obj)}"

    @mark.dependency(depends=["equality", "rotate_cw", "rotate_ccw"])
    @given(data())
    def test_3ccw_cw_equivalence(self, data):
        obj = data.draw(self.objs)
        gold = deepcopy(obj).rotate_cw()
        obj = obj.rotate_ccw().rotate_ccw().rotate_ccw()
        assert obj == gold, f"failed for {str(obj)}\n{repr(obj)}"

    @mark.dependency(depends=["objs_minus_c4", "inequality", "rotate_cw"])
    @given(data())
    def test_cw_non_idempotence(self, data):
        obj = data.draw(self.objs_minus_c4)
        obj_copy = deepcopy(obj).rotate_cw()
        assert obj != obj_copy, f"failed for {str(obj)}\n{repr(obj)}"

    @mark.dependency(depends=["objs_minus_c4", "inequality", "rotate_ccw"])
    @given(data())
    def test_ccw_non_idempotence(self, data):
        obj = data.draw(self.objs_minus_c4)
        obj_copy = deepcopy(obj).rotate_ccw()
        assert obj != obj_copy, f"failed for {str(obj)}\n{repr(obj)}"

    @mark.dependency(depends=["objs_minus_c2", "inequality", "rotate_ht"])
    @given(data())
    def test_ht_non_idempotence(self, data):
        obj = data.draw(self.objs_minus_c2)
        obj_copy = deepcopy(obj).rotate_ht()
        assert obj != obj_copy, f"failed for {str(obj)}\n{repr(obj)}"

    @mark.dependency(
        depends=[
            "equality",
            "deepcopy",
            "rotate_cw",
            "rotate_ccw",
            "rotate_ht",
            "objs_minus_c2",
        ]
    )
    @given(data())
    def test_get_iso_transform(self, data):
        a = data.draw(self.objs_minus_c2)

        b = deepcopy(a)
        assert a == b
        transformation = a.get_iso_transform(b)
        err_str = f"{a}:\n{repr(a)}\n{transformation}"
        assert transformation == RotationEnum.NOTHING, err_str

        b = deepcopy(a).rotate_cw()
        assert a != b
        transformation = a.get_iso_transform(b)
        err_str = f"{a}:\n{repr(a)}\n{transformation}"
        assert transformation == RotationEnum.CW, err_str

        b = deepcopy(a).rotate_ccw()
        assert a != b
        transformation = a.get_iso_transform(b)
        err_str = f"{a}:\n{repr(a)}\n{transformation}"
        assert transformation == RotationEnum.CCW, err_str

        b = deepcopy(a).rotate_ht()
        assert a != b
        transformation = a.get_iso_transform(b)
        err_str = f"{a}:\n{repr(a)}\n{transformation}"
        assert transformation == RotationEnum.HT, err_str

        c = data.draw(self.objs_minus_c4)
        transformation = a.get_iso_transform(c)
        err_str = f"{a}:\n{repr(a)}\n{c}:\n{repr(c)}\n{transformation}"
        if transformation is None:
            for _ in range(4):
                a = a.rotate_cw()
                assert a != c, err_str
        else:
            verified_isomorphic = False
            for _ in range(4):
                a = a.rotate_cw()
                if a == c:
                    verified_isomorphic = True
                    break
            assert verified_isomorphic, err_str

    @mark.dependency(
        depends=[
            "equality",
            "deepcopy",
            "rotate_cw",
            "rotate_ccw",
            "rotate_ht",
            "objs_minus_c4",
        ]
    )
    @given(data())
    def test_rotate(self, data):
        a = data.draw(self.objs)
        b = deepcopy(a)

        assert a.rotate(RotationEnum.NOTHING) == b
        assert a.rotate_cw().rotate(RotationEnum.CCW) == b
        assert a.rotate_ht().rotate(RotationEnum.HT) == b
        assert a.rotate_ccw().rotate(RotationEnum.CW) == b

        with raises(AssertionError):
            a.rotate(None)

        with raises(Exception):
            a.rotate(12)
