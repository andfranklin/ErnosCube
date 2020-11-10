from ErnosCube.cube import Cube
from copy import deepcopy


class RotationContext:
    def __init__(self, cube, rotation):
        self.cube = cube
        self.rotation = rotation

    def __enter__(self):
        self.cube.rotate(self.rotation)
        return self.cube

    def __exit__(self, type, value, traceback):
        self.cube.rotate(self.rotation.inverse())


class MutatedCube:
    def __init__(self, cube, parent=None, rotation=None, rotation_sequence=None):
        self.cube = deepcopy(cube)
        self.parent = parent
        self.rotation = rotation
        self.children = []

        if self.parent is None:
            assert self.rotation is None
            assert rotation_sequence is None
            self.rotation_sequence = []
        else:
            assert self.rotation is not None
            self.parent.children.append(self)
            if rotation_sequence is None:
                self.rotation_sequence = self.make_rotation_sequence(rotation)
            else:
                self.rotation_sequence = rotation_sequence

    def make_rotation_sequence(self, rotation):
        if self.parent is None:
            return [rotation]
        else:
            return [*self.rotation_sequence, rotation]


class LayeredArray:
    def __init__(self):
        self.data = []
        self.start_indices = [0]

    def append(self, thing):
        self.data.append(thing)

    def close_layer(self):
        start_index = len(self.data)
        assert start_index >= self.start_indices[-1]
        self.start_indices.append(start_index)

    def get_layer_slice(self, layer_index):
        assert layer_index < len(self.start_indices)
        start = self.start_indices[layer_index]
        end = self.start_indices[layer_index + 1]
        return slice(start, end)

    def get_layer_size(self, layer_index):
        layer_slice = self.get_layer_slice(layer_index)
        return layer_slice.stop - layer_slice.start

    def get_layer(self, layer_index):
        layer_slice = self.get_layer_slice(layer_index)
        return self.data[layer_slice]


def is_duplicate(rot_seq, duplic_mut_seqs):
    for duplic_mut_seq in duplic_mut_seqs.data:
        layer = len(duplic_mut_seq)
        rots_iterator = zip(duplic_mut_seq, rot_seq[-layer:])
        if all(duplic_rot == rot for duplic_rot, rot in rots_iterator):
            return True
    return False


def is_essentially_unique(cube, unique_cubes):
    for unique_cube in unique_cubes.data:
        if cube.is_isomorphic(unique_cube.cube):
            return False
    return True


def expand_layer(layer, unique_cubes, dup_mut_seqs):
    parents = unique_cubes.get_layer(layer - 1)
    rotations = parents[0].cube.get_atomic_mutations()
    for parent in parents:
        parent_cube_copy = deepcopy(parent.cube)
        for rotation in rotations:
            rot_seq = parent.make_rotation_sequence(rotation)
            if is_duplicate(rot_seq, dup_mut_seqs):
                dup_mut_seqs.append(rot_seq)

            else:
                with RotationContext(parent_cube_copy, rotation) as candidate:
                    if is_essentially_unique(candidate, unique_cubes):
                        child = MutatedCube(
                            candidate,
                            parent=parent,
                            rotation=rotation,
                            rotation_sequence=rot_seq,
                        )
                        unique_cubes.append(child)
                    else:
                        dup_mut_seqs.append(rot_seq)
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


def expand_mutation_tree(cube_size, n_layers, verbose=False):
    root_cube = Cube(N=cube_size)

    unique_cubes = LayeredArray()
    unique_cubes.append(MutatedCube(root_cube))
    unique_cubes.close_layer()

    dup_mut_seqs = LayeredArray()
    dup_mut_seqs.close_layer()

    for layer in range(1, n_layers + 1):
        expand_layer(layer, unique_cubes, dup_mut_seqs)
        if verbose:
            print_layer_expansion_info(layer, unique_cubes, dup_mut_seqs)

    return unique_cubes.data[0]


if __name__ == "__main__":
    cube_size = 2
    n_layers = 3
    verbose = True
    root = expand_mutation_tree(cube_size, n_layers, verbose=verbose)
