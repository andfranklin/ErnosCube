from ErnosCube.expand_mutation_tree import _is_duplicate
from ErnosCube.expand_mutation_tree import _is_essentially_unique
from ErnosCube.expand_mutation_tree import _print_layer_expansion_info
from ErnosCube.expand_mutation_tree import _expand_layer
from ErnosCube.expand_mutation_tree import expand_mutation_tree

from ErnosCube.cube_mutation import CubeMutation
from ErnosCube.axis_enum import AxisEnum
from ErnosCube.rotation_enum import RotationEnum

from ErnosCube.layered_array import LayeredArray
from ErnosCube.cube import Cube
from ErnosCube.mutated_cube import MutatedCube
from ErnosCube.mutation_node import MutationNode

from copy import deepcopy
from pytest import mark


class TestExpandMutationTree:
    """Collection of all tests run on the `expand_mutation_tree` function."""

    @mark.dependency(name="is_duplicate")
    def test_is_duplicate(self):
        mut_seq = [
            CubeMutation(AxisEnum.X, RotationEnum.CW, 0),
            CubeMutation(AxisEnum.Y, RotationEnum.HT, 1),
        ]

        dup_mut_seq = LayeredArray()
        dup_mut_seq.append([CubeMutation.e])

        assert not _is_duplicate(mut_seq, dup_mut_seq)

        dup_mut_seq.close_layer()
        dup_mut_seq.append(mut_seq)
        dup_mut_seq.close_layer()

        assert _is_duplicate(mut_seq, dup_mut_seq)

    @mark.dependency(name="is_essentially_unique")
    def test_is_essentially_unique(self):
        cube = Cube(N=3)

        unique_cubes = LayeredArray()
        unique_cubes.append(MutatedCube(cube, None))
        unique_cubes.close_layer()

        assert not _is_essentially_unique(cube, 1, unique_cubes)

        mutation = CubeMutation(AxisEnum.X, RotationEnum.CW, 0)
        mutated_cube = deepcopy(cube)
        mutated_cube.mutate(mutation)

        assert _is_essentially_unique(mutated_cube, 1, unique_cubes)

        unique_cubes.append(MutatedCube(mutated_cube, mutation))

        assert not _is_essentially_unique(mutated_cube, 1, unique_cubes)

        mutated_cube_2 = deepcopy(mutated_cube)
        mutated_cube_2.mutate(CubeMutation(AxisEnum.Z, RotationEnum.HT, -1))

        assert not _is_essentially_unique(mutated_cube_2, 1, unique_cubes)

    @mark.dependency(name="print_layer_expansion_info")
    def test_print_layer_expansion_info(self):
        cube = Cube(N=3)

        unique_cubes = LayeredArray()
        mutation_node = MutationNode(None, None, None)
        unique_cubes.append(MutatedCube(cube, mutation_node))
        unique_cubes.close_layer()

        dup_mut_seqs = LayeredArray()
        dup_mut_seqs.close_layer()

        _print_layer_expansion_info(True, 0, unique_cubes, dup_mut_seqs)
        _print_layer_expansion_info(False, 0, unique_cubes, dup_mut_seqs)

    @mark.dependency(
        name="expand_layer_1",
        depends=["is_duplicate", "is_essentially_unique", "print_layer_expansion_info"],
    )
    def test_expand_layer(self):
        cube = Cube(N=2)
        mutation_basis = cube.get_nonisomorphic_mutations()

        unique_cubes = LayeredArray()
        mutation_node = MutationNode(None, None, None)
        unique_cubes.append(MutatedCube(cube, mutation_node))
        unique_cubes.close_layer()

        dup_mut_seqs = LayeredArray()
        dup_mut_seqs.close_layer()

        _expand_layer(1, mutation_basis, unique_cubes, dup_mut_seqs)

        assert unique_cubes.get_layer_size(1) == 9
        assert dup_mut_seqs.get_layer_size(1) == 9

    @mark.slow
    @mark.dependency(name="expand_layer_2", depends=["expand_layer_1"])
    def test_expand_layer_2(self):
        cube = Cube(N=2)
        mutation_basis = cube.get_nonisomorphic_mutations()

        unique_cubes = LayeredArray()
        mutation_node = MutationNode(None, None, None)
        unique_cubes.append(MutatedCube(cube, mutation_node))
        unique_cubes.close_layer()

        dup_mut_seqs = LayeredArray()
        dup_mut_seqs.close_layer()

        _expand_layer(1, mutation_basis, unique_cubes, dup_mut_seqs)
        _expand_layer(2, mutation_basis, unique_cubes, dup_mut_seqs)

        assert unique_cubes.get_layer_size(2) == 54
        assert dup_mut_seqs.get_layer_size(2) == 108

    @mark.dependency(name="expand_mutation_tree_1", depends=["expand_layer_1"])
    def test_expand_mutation_tree_1(self):
        cube = Cube(N=1)
        mutation_basis = cube.get_nonisomorphic_mutations()
        mut_cube = expand_mutation_tree(cube, mutation_basis, 10, verbose=False)

        assert mut_cube.cube == cube
        assert mut_cube.cube is not cube

        assert mut_cube.mutation_node.parent is None
        assert mut_cube.mutation_node.mutation is None
        assert len(mut_cube.mutation_node.children) == 0

    @mark.dependency(name="expand_mutation_tree_2", depends=["expand_layer_1"])
    def test_expand_mutation_tree_2(self):
        cube = Cube(N=2)
        mutation_basis = cube.get_nonisomorphic_mutations()
        mut_cube = expand_mutation_tree(cube, mutation_basis, 1, verbose=False)

        assert mut_cube.cube == cube
        assert mut_cube.cube is not cube

        assert mut_cube.mutation_node.parent is None
        assert mut_cube.mutation_node.mutation is None
        assert len(mut_cube.mutation_node.children) == 9

        for child in mut_cube.mutation_node.children:
            assert child.parent is mut_cube.mutation_node
            assert child.mutation in mutation_basis
            assert len(child.children) == 0
            assert len(child.mut_seq) == 1
            assert child.mut_seq[0] == child.mutation

    @mark.slow
    @mark.dependency(name="expand_mutation_tree_2_slow", depends=["expand_layer_1"])
    def test_expand_mutation_tree_2_slow(self):
        cube = Cube(N=2)
        mutation_basis = cube.get_nonisomorphic_mutations()
        mut_cube = expand_mutation_tree(cube, mutation_basis, 2, verbose=False)

        layer_2_children = []
        for child in mut_cube.mutation_node.children:
            layer_2_children.extend(child.children)

        assert len(layer_2_children) == 54
        for child in layer_2_children:
            assert child.parent is not mut_cube.mutation_node
            assert child.mutation in mutation_basis
            assert len(child.children) == 0
            assert len(child.mut_seq) == 2
            assert child.mut_seq[-1] == child.mutation
