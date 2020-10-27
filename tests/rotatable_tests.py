from hypothesis import given
from hypothesis.strategies import data


class RotatableTests:
	"""A test suite of property tests for Rotatable classes of objects.

	This class implements a suit of general tests that all rotatable objects
	should pass. A test suit for a specific rotatable class can incorporate
	this tests by inheriting this class and by specifying the member variable
	`rotatable_objs` with a hypothesis strategy.
	"""

	@given(data())
	def test_cw_ccw_invertability(self, data):
		rotatable_obj = data.draw(self.rotatable_objs)
		assert rotatable_obj.rotate_cw().rotate_ccw() == rotatable_obj
		assert rotatable_obj.rotate_ccw().rotate_cw() == rotatable_obj