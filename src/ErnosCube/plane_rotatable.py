from abc import ABC, abstractmethod
from .rotation_enum import RotationEnum


class PlaneRotatable(ABC):
    """ABC for objects that exist in a plane, and can be rotated.

    Classes that inherit from this base class must override the methods
    decorated with `@abstractmethod`.
    """

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
        return not (self == other)

    def rotate_cw(self):
        """Applys a clockwise rotation.

        Warning: this method might mutate the object. In general, it returns
        the object so that multiple rotations can be chained together.
        """
        return self._rotate_cw()

    def rotate_ccw(self):
        """Applys a counter-clockwise rotation.

        Warning: this method might mutate the object. In general, it returns
        the object so that multiple rotations can be chained together.
        """
        return self._rotate_ccw()

    def rotate_ht(self):
        """Applys a half-turn rotation.

        Warning: this method might mutate the object. In general, it returns
        the object so that multiple rotations can be chained together.
        """
        return self._rotate_ht()

    @abstractmethod
    def _rotate_cw(self):
        raise NotImplementedError

    @abstractmethod
    def _rotate_ccw(self):
        raise NotImplementedError

    @abstractmethod
    def _rotate_ht(self):
        raise NotImplementedError

    def get_iso_transform(self, other):
        """Returns the isomorphic transfomation to reach the argument object.

        The transformation is encoded as a `RotationEnum`. If there is no
        isomorphic transformation between the two faces then this function
        returns `None`.
        """
        if self == other:
            return RotationEnum.NOTHING

        rotated_self = self.rotate_cw()
        if rotated_self == other:
            rotated_self = rotated_self.rotate_ccw()
            return RotationEnum.CW

        rotated_self = rotated_self.rotate_cw()
        if rotated_self == other:
            rotated_self = rotated_self.rotate_ht()
            return RotationEnum.HT

        rotated_self = rotated_self.rotate_cw()
        if rotated_self == other:
            rotated_self = rotated_self.rotate_cw()
            return RotationEnum.CCW

        rotated_self = rotated_self.rotate_cw()
        return None

    def rotate(self, rotation_enum):
        """Appropriately rotates a PlaneRotatable provided a `RotationEnum`.

        Returns `self` so that rotations can be chained together.
        """
        assert rotation_enum is not None

        if rotation_enum == RotationEnum.NOTHING:
            return self

        elif rotation_enum == RotationEnum.CW:
            return self.rotate_cw()

        elif rotation_enum == RotationEnum.HT:
            return self.rotate_ht()

        elif rotation_enum == RotationEnum.CCW:
            return self.rotate_ccw()

        else:
            err_str = f"unexpected argument ({rotation_enum}) used in "
            err_str += "`PlaneRotatable.rotate`."
            raise Exception(err_str)
