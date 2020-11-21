from .layered_array import LayeredArray
from .mutation_node import MutationNode
from .mutated_cube import MutatedCube
from copy import deepcopy


def _is_duplicate(mut_seq, dup_mut_seqs):
    """Returns `True` if `mut_seq` is a duplicate.

    Args:
        mut_seq (list(:obj:`CubeMutation`)): The :obj:`list` of
            :obj:`CubeMutation`s which is being checked.
        dup_mut_seqs (:obj:`LayeredArray`): All lists of :obj:`CubeMutation`s
            which have been explored thus far.

    Returns:
        bool: True if `mut_seq` is a duplicate, False otherwise.
    """
    for dup_mut_seq in dup_mut_seqs.data:
        layer = len(dup_mut_seq)
        muts_iterator = zip(dup_mut_seq, mut_seq[-layer:])
        if all(duplic_mut == mut for duplic_mut, mut in muts_iterator):
            return True
    return False


def _is_essentially_unique(cube, layer, unique_cubes):
    """Returns `True` if the cube is, so far, essentially unique.

    In general, a cube is essentially unique in comparison with a collection of
    cubes if it is not isomorphic to any of the cubes in the collection.

    A naïve implementation of this function would compare the candidate with
    every cube inserted into the mutation tree thus far. This function does not
    do that. Rather, the cube is compared with all cubes inserted thus far in
    the current layer, and all cubes in the previous two layers.

    Justification: In general, a cube at layer N (for N>0) mutated by 1 turn
    may result in a cube at layer N-1, N or N+1. A candidate cube at layer N+1
    only needs to be compared against the previous 2 layers since it is
    impossible that a cube isomorphic to the candidate would exist in layer
    N-2.

    Args:
        cube (:obj:`Cube`): The :obj:`Cube` that is being checked if it is
            essentially unique.
        layer (int): The layer number for which the cube might belong.
        unique_cubes (:obj:`LayeredArray`): Collection of all unique
            :obj:`MutatedCube`s.

    Returns:
        bool: True if `cube` is essentially unique, False otherwise.
    """
    minimum_layer = max(0, layer - 2)
    comparison_start = unique_cubes.get_layer_slice(minimum_layer).start
    for unique_cube in unique_cubes.data[comparison_start:]:
        if cube.is_isomorphic(unique_cube.cube):
            return False
    return True


def _print_layer_expansion_info(verbose, layer, unique_cubes, dup_mut_seqs):
    """Provies command-line feedback.

    Args:
        verbose (bool): True if printout is desired, otherwise False.
        layer (int): Integer of the layer for which the info is being printed.
        unique_cubes (:obj:`LayeredArray`): All of the unique cubes discovered
            thus far.
        dup_mut_seqs (:obj:`LayeredArray`): All of the duplicate mutation
            sequences discovered thus far.
    """
    if verbose:
        n_new_mutations = unique_cubes.get_layer_size(layer)
        n_dup_mutations = dup_mut_seqs.get_layer_size(layer)
        possible_mutations = n_new_mutations + n_dup_mutations
        uniqueness_ratio = n_new_mutations / possible_mutations

        print(f"Layer {layer}")
        print(f"{n_new_mutations} new unique mutations")
        print(f"uniqueness ratio", uniqueness_ratio)
        print(f"{len(unique_cubes.data)} total unique cubes")
        print()


def _expand_layer(layer, mutation_basis, unique_cubes, dup_mut_seqs):
    """Expands a layer of the mutation tree provided a proceeding layer.

    The expansion only includes mutated cubes which are essentially unique. A
    quick check to check for possibly duplicate cubes is done by
    `_is_duplicate` before an exhaustive check is done by
    `_is_essentially_unique`.

    Args:
        layer (int): The layer number being expanded. It is assumed that all
            layers < layer have already been expanded.
        mutation_basis (list(:obj:`CubeMutation`)): Collection of CubeMutations
            that form the basis for how the cube can be mutated. It is the
            responsibility of the caller to ensure that the `mutation_basis`
            spans space with which they  wish to explore.
        unique_cubes (:obj:`LayeredArray`): All of the unique cubes discovered
            thus far.
        dup_mut_seqs (:obj:`LayeredArray`): All of the duplicate mutation
            sequences discovered thus far.
    """
    assert layer > 0
    parents = unique_cubes.get_layer(layer - 1)
    for parent in parents:
        candidate = deepcopy(parent.cube)
        for mutation in mutation_basis:
            mut_seq = parent.mutation_node.make_mut_seq(mutation)
            if _is_duplicate(mut_seq, dup_mut_seqs):
                dup_mut_seqs.append(mut_seq)  # `--runslow` to cover

            else:
                candidate.mutate(mutation)
                if _is_essentially_unique(candidate, layer, unique_cubes):
                    mutation_node = MutationNode(
                        parent.mutation_node, mutation, mut_seq
                    )
                    child = MutatedCube(deepcopy(candidate), mutation_node)
                    unique_cubes.append(child)
                else:
                    dup_mut_seqs.append(mut_seq)
                candidate.mutate(mutation.inverse())
    unique_cubes.close_layer()
    dup_mut_seqs.close_layer()


def expand_mutation_tree(root_cube, mutation_basis, n_layers, verbose=False):
    """Expands the mutation tree by at most `n_layers`.

    The MutationNodes of the resulting mutation tree should be identical for a
    given cube size regardless of which `root_cube` is used.

    Args:
        root_cube (:obj:`Cube`): The initial cube from which the mutation tree
            will be built from.
        mutation_basis (list(:obj:`CubeMutation`)): Collection of CubeMutations
            that form the basis for how the cube can be mutated. It is the
            responsibility of the caller to ensure that the `mutation_basis`
            spans space with which they  wish to explore.
        n_layers (int): The desired number of layers to be expanded.
        verbose (bool, optional): True if printout is desired, otherwise False.

    Returns:
        :obj:`MutatedCube`: The mutated cube at the root of the mutation tree.
    """
    unique_cubes = LayeredArray()
    mutation_node = MutationNode(None, None, None)
    unique_cubes.append(MutatedCube(deepcopy(root_cube), mutation_node))
    unique_cubes.close_layer()

    dup_mut_seqs = LayeredArray()
    dup_mut_seqs.close_layer()

    for layer in range(1, n_layers + 1):
        _expand_layer(layer, mutation_basis, unique_cubes, dup_mut_seqs)
        _print_layer_expansion_info(verbose, layer, unique_cubes, dup_mut_seqs)
        if unique_cubes.get_layer_size(layer) == 0:
            break

    return unique_cubes.data[0]
