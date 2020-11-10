from ErnosCube.cube import Cube
from copy import deepcopy

N = 2
root_cube = Cube(N=N)


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


def is_duplicate(rot_seq):
    for i, duplic_rot_seq in enumerate(duplic_rot_seqs):
        layer = len(duplic_rot_seq)
        rots_iterator = zip(duplic_rot_seq, rot_seq[-layer:])
        if all(duplic_rot == rot for duplic_rot, rot in rots_iterator):
            return True
    return False


def is_essentially_unique(cube):
    for unique_cube in unique_cubes:
        if cube.is_isomorphic(unique_cube.cube):
            return False
    return True


isomorphic_rotations = root_cube.get_isomorphic_rotations()
atomic_mutations = root_cube.get_atomic_mutations()
atomic_rotations = root_cube.get_all_atomic_rotations()

print(f"{len(isomorphic_rotations)} isomorphic rotations")
print(f"{len(atomic_rotations)} atomic rotations")
print()

layer = 0
unique_cubes = [MutatedCube(root_cube)]
unique_layer_starts = [0, 1]

duplic_rot_seqs = []
duplic_layer_starts = [0]


def unique_layer_slice(layer_indx):
    start = unique_layer_starts[layer_indx]
    end = unique_layer_starts[layer_indx + 1]
    return slice(start, end)


def unique_cubes_layer(layer_indx):
    return unique_cubes[unique_layer_slice(layer_indx)]


def duplic_layer_slice(layer_indx):
    assert layer_indx > 0
    start = duplic_layer_starts[layer_indx - 1]
    end = duplic_layer_starts[layer_indx]
    return slice(start, end)


def duplic_rot_seqs_layer(layer_indx):
    return duplic_rot_seqs[duplic_layer_slice(layer_indx)]


def expand_layer(layer):
    parents = unique_cubes_layer(layer - 1)
    rotations = parents[0].cube.get_atomic_mutations()
    for parent in parents:
        parent_cube_copy = deepcopy(parent.cube)
        for rotation in rotations:
            rot_seq = parent.make_rotation_sequence(rotation)
            if is_duplicate(rot_seq):
                duplic_rot_seqs.append(rot_seq)

            else:
                with RotationContext(parent_cube_copy, rotation) as candidate:
                    if is_essentially_unique(candidate):
                        child = MutatedCube(
                            candidate,
                            parent=parent,
                            rotation=rotation,
                            rotation_sequence=rot_seq,
                        )
                        unique_cubes.append(child)
                    else:
                        duplic_rot_seqs.append(rot_seq)
    unique_layer_starts.append(len(unique_cubes))
    duplic_layer_starts.append(len(duplic_rot_seqs))


def print_layer_expansion_info(layer):
    n_new_mutations = len(unique_cubes_layer(layer))
    n_dup_mutations = len(duplic_rot_seqs_layer(layer))
    possible_mutations = n_new_mutations + n_dup_mutations
    uniqueness_ratio = n_new_mutations / possible_mutations

    print(f"Layer {layer}")
    print(f"{n_new_mutations} new unique mutations")
    print(f"uniqueness ratio", uniqueness_ratio)
    print(f"{len(unique_cubes)} total unique cubes")
    print()


for layer in range(1, 4):
    expand_layer(layer)
    print_layer_expansion_info(layer)
