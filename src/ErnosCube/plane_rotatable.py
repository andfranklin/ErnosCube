from abc import ABC, abstractmethod


class PlaneRotatable(ABC):
	"""Abstract base class for objects that exist in a plane, and can be rotated.

	Classes that inherit from this base class must override the methods decorated
	with `@abstractmethod`.
	"""

	@abstractmethod
	def rotate_cw(self):
		pass

	@abstractmethod
	def rotate_ccw(self):
		pass

	@abstractmethod
	def rotate_ht(self):
		pass