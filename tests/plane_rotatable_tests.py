from hypothesis import given
from hypothesis.strategies import data
from copy import deepcopy


class PlaneRotatableTests:
    """A test suite of property tests for PlaneRotatable classes of objects.

    This class implements a suit of general tests that all rotatable objects
    are expected to pass. A test suit for a specific rotatable class can
    incorporate this tests by inheriting this class and by specifying the
    member variable `plane_rotatable_objs` with a hypothesis strategy.
    """

    @given(data())
    def test_copyability_and_equality(self, data):
        obj = data.draw(self.plane_rotatable_objs)
        obj_copy = deepcopy(obj)
        assert obj == obj_copy

    @given(data())
    def test_cw_invertability(self, data):
        obj = data.draw(self.plane_rotatable_objs)
        gold = deepcopy(obj)
        assert obj.rotate_cw().rotate_cw().rotate_cw().rotate_cw() == gold

    @given(data())
    def test_ccw_invertability(self, data):
        obj = data.draw(self.plane_rotatable_objs)
        gold = deepcopy(obj)
        assert obj.rotate_ccw().rotate_ccw().rotate_ccw().rotate_ccw() == gold

    @given(data())
    def test_ht_invertability(self, data):
        obj = data.draw(self.plane_rotatable_objs)
        gold = deepcopy(obj)
        assert obj.rotate_ht().rotate_ht() == gold

    @given(data())
    def test_cw_ccw_invertability(self, data):
        obj = data.draw(self.plane_rotatable_objs)
        gold = deepcopy(obj)
        assert obj.rotate_cw().rotate_ccw() == gold
        assert obj.rotate_ccw().rotate_cw() == gold

    @given(data())
    def test_ht_2cw_equivalence(self, data):
        obj = data.draw(self.plane_rotatable_objs)
        obj_copy = deepcopy(obj)
        assert obj.rotate_ht() == obj_copy.rotate_cw().rotate_cw()

    @given(data())
    def test_ht_2ccw_equivalence(self, data):
        obj = data.draw(self.plane_rotatable_objs)
        obj_copy = deepcopy(obj)
        assert obj.rotate_ht() == obj_copy.rotate_ccw().rotate_ccw()
