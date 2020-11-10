from .cube_rotation import CubeRotation


class CubeRotationSequence:
    def __init__(self, *rotations):
        self.rotations = list(rotations)

    def append(self, cube_rotation):
        assert isinstance(cube_rotation, CubeRotation)
        self.rotations.append(cube_rotation)

    def extend(self, cube_rotations):
        assert isinstance(cube_rotations, (CubeRotationSequence, list))

        if isinstance(cube_rotations, CubeRotationSequence):
            self.rotations.extend(cube_rotations.rotations)
        else:
            self.rotations.extend(cube_rotations)

    def __add__(self, other):
        assert isinstance(other, (CubeRotationSequence, list))

        if isinstance(other, CubeRotationSequence):
            rotations = self.rotations + other.rotations
        else:
            rotations = self.rotations + other

        return CubeRotationSequence(*rotations)

    def __radd__(self, other):
        assert isinstance(other, list)
        other = CubeRotationSequence(*other)
        return other + self
