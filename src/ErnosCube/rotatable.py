from abc import ABC, abstractmethod
from enum import Enum


class EnumABCMeta(type(Enum), type(ABC)):
	pass


class Rotatable(ABC):
	@abstractmethod
	def rotate_cw(self):
		pass

	@abstractmethod
	def rotate_ccw(self):
		pass

	@abstractmethod
	def rotate_ht(self):
		pass