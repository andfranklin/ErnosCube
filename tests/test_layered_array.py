from ErnosCube.layered_array import LayeredArray

from pytest import mark, raises
from hypothesis import given
from hypothesis.strategies import integers


class TestLayeredArray:
    """Collection of all tests run on instances of the LayeredArray."""

    @mark.dependency(name="construction")
    def test_construction(self):
        LayeredArray()

    @mark.dependency(name="append", depends=["construction"])
    @given(integers())
    def test_append(self, integer):
        la = LayeredArray()
        assert len(la.data) == 0
        assert len(la.start_indices) == 1
        la.append(integer)
        assert len(la.data) == 1
        assert len(la.start_indices) == 1

    @mark.dependency(name="close_layer", depends=["construction"])
    def test_close_layer(self):
        la = LayeredArray()
        assert len(la.data) == 0
        assert len(la.start_indices) == 1
        la.close_layer()
        assert len(la.data) == 0
        assert len(la.start_indices) == 2

    @mark.dependency(name="get_layer_slice", depends=["close_layer"])
    def test_get_layer_slice(self):
        la = LayeredArray()
        la.close_layer()
        layer_slice = la.get_layer_slice(0)
        assert layer_slice.start == 0
        assert layer_slice.stop == 0

    @mark.dependency(name="get_layer_slice_fail", depends=["construction"])
    def test_get_layer_slice_fail(self):
        la = LayeredArray()
        with raises(IndexError):
            la.get_layer_slice(0)

    @mark.dependency(name="get_layer_size", depends=["get_layer_slice"])
    @given(integers(), integers())
    def test_get_layer_size(self, a, b):
        la = LayeredArray()
        la.close_layer()
        la.append(a)
        la.append(b)
        la.close_layer()
        assert len(la.data) == 2
        assert len(la.start_indices) == 3
        assert la.get_layer_size(0) == 0
        assert la.get_layer_size(1) == 2

    @mark.dependency(name="get_layer", depends=["get_layer_slice"])
    @given(integers(), integers())
    def test_get_layer(self, a, b):
        la = LayeredArray()
        la.close_layer()
        la.append(a)
        la.append(b)
        la.close_layer()
        assert len(la.data) == 2
        assert len(la.start_indices) == 3
        assert la.get_layer(0) == []
        assert la.get_layer(1) == [a, b]
