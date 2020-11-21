from ErnosCube.cube import Cube
from ErnosCube.layered_array import LayeredArray
from ErnosCube.mutation_node import MutationNode
from copy import deepcopy


class MutatedCube:
    def __init__(self, cube, mutation_node):
        self.cube = cube
        self.mutation_node = mutation_node


def is_duplicate(mut_seq, dup_mut_seqs):
    for dup_mut_seq in dup_mut_seqs.data:
        layer = len(dup_mut_seq)
        muts_iterator = zip(dup_mut_seq, mut_seq[-layer:])
        if all(duplic_mut == mut for duplic_mut, mut in muts_iterator):
            return True
    return False


def is_essentially_unique(candidate, layer, unique_cubes):
    """This function returns True if the cube is, so far, essentially unique.

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
    """
    minimum_layer = max(0, layer - 2)
    comparison_start = unique_cubes.get_layer_slice(minimum_layer).start
    for unique_cube in unique_cubes.data[comparison_start:]:
        if candidate.is_isomorphic(unique_cube.cube):
            return False
    return True


def expand_layer(layer, mutation_basis, unique_cubes, dup_mut_seqs):
    parents = unique_cubes.get_layer(layer - 1)
    for parent in parents:
        candidate = deepcopy(parent.cube)
        for mutation in mutation_basis:
            mut_seq = parent.mutation_node.make_mut_seq(mutation)
            if is_duplicate(mut_seq, dup_mut_seqs):
                dup_mut_seqs.append(mut_seq)

            else:
                candidate.mutate(mutation)
                if is_essentially_unique(candidate, layer, unique_cubes):
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


def print_layer_expansion_info(layer, unique_cubes, dup_mut_seqs):
    n_new_mutations = unique_cubes.get_layer_size(layer)
    n_dup_mutations = dup_mut_seqs.get_layer_size(layer)
    possible_mutations = n_new_mutations + n_dup_mutations
    uniqueness_ratio = n_new_mutations / possible_mutations

    print(f"Layer {layer}")
    print(f"{n_new_mutations} new unique mutations")
    print(f"uniqueness ratio", uniqueness_ratio)
    print(f"{len(unique_cubes.data)} total unique cubes")
    print()


def expand_mutation_tree(root_cube, mutation_basis, n_layers, verbose=False):
    unique_cubes = LayeredArray()
    mutation_node = MutationNode(None, None, None)
    unique_cubes.append(MutatedCube(deepcopy(root_cube), mutation_node))
    unique_cubes.close_layer()

    dup_mut_seqs = LayeredArray()
    dup_mut_seqs.close_layer()

    for layer in range(1, n_layers + 1):
        expand_layer(layer, mutation_basis, unique_cubes, dup_mut_seqs)
        if verbose:
            print_layer_expansion_info(layer, unique_cubes, dup_mut_seqs)

    return unique_cubes.data[0]


if __name__ == "__main__":
    cube_size = 2
    n_layers = 3

    # cube_size = 3
    # n_layers = 2

    verbose = True
    root_cube = Cube(N=cube_size)

    mutation_basis = root_cube.get_nonisomorphic_mutations()
    # mutation_basis = = root_cube.get_face_mutations()  # use to verify with Korf, 1997

    root = expand_mutation_tree(root_cube, mutation_basis, n_layers, verbose=verbose)
