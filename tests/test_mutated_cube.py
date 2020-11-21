from ErnosCube.cube import Cube
from ErnosCube.mutation_node import MutationNode
from ErnosCube.mutated_cube import MutatedCube
from pytest import mark


class TestMutatedCube:
    """Collection of all tests run on instances of the MutatedCube."""

    @mark.dependency(name="construction")
    def test_construction(self):
        cube = Cube(N=2)
        mutation_node = MutationNode(None, None, None)
        MutatedCube(cube, mutation_node)
