from ErnosCube.mutation_node import MutationNode
from ErnosCube.cube_mutation import CubeMutation
from pytest import mark


class TestMutationNode:
    """Collection of all tests run on instances of the MutationNode."""

    @mark.dependency(name="construction_1")
    def test_construction_1(self):
        MutationNode(None, None, None)

    @mark.dependency(name="make_mut_seq_1", depends=["construction_1"])
    def test_make_mut_seq_1(self):
        root = MutationNode(None, None, None)
        mut_seq = root.make_mut_seq(CubeMutation.e)
        assert len(mut_seq) == 1
        assert mut_seq[0] == CubeMutation.e

    @mark.dependency(
        name="construction_2", depends=["construction_1", "make_mut_seq_1"]
    )
    def test_construction_2(self):
        root = MutationNode(None, None, None)

        mutation = CubeMutation.e
        mut_seq = root.make_mut_seq(mutation)
        child = MutationNode(root, mutation, mut_seq)

        assert root.parent is None
        assert root.mutation is None
        assert len(root.children) == 1
        assert root.children[0] == child
        assert len(root.mut_seq) == 0

        assert child.parent is root
        assert child.mutation == mutation
        assert len(child.children) == 0
        assert len(child.mut_seq) == 1
        assert child.mut_seq[0] == mutation

    @mark.dependency(name="make_mut_seq_2", depends=["construction_2"])
    def test_make_mut_seq_2(self):
        root = MutationNode(None, None, None)

        mutation = CubeMutation.e
        mut_seq = root.make_mut_seq(mutation)
        child = MutationNode(root, mutation, mut_seq)
        mut_seq_2 = child.make_mut_seq(mutation)

        assert len(mut_seq_2) == 2
        assert mut_seq_2[0] == mutation
        assert mut_seq_2[1] == mutation
