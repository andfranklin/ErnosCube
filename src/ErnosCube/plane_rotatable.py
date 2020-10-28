from abc import ABC, abstractmethod


class PlaneRotatable(ABC):
    """Abstract base class for objects that exist in a plane, and can be rotated.

    Classes that inherit from this base class must override the methods decorated
    with `@abstractmethod`.
    """

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
        return not (self == other)

    @abstractmethod
    def rotate_cw(self):
        raise NotImplementedError

    @abstractmethod
    def rotate_ccw(self):
        raise NotImplementedError

    @abstractmethod
    def rotate_ht(self):
        raise NotImplementedError
