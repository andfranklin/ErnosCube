from ErnosCube.cube import Cube
from ErnosCube.expand_mutation_tree import expand_mutation_tree

# cube_size = 1
# n_layers = 10

cube_size = 2
n_layers = 3

# cube_size = 3
# n_layers = 2

verbose = True
root_cube = Cube(N=cube_size)

mutation_basis = root_cube.get_nonisomorphic_mutations()
# mutation_basis = = root_cube.get_face_mutations()  # use to verify with Korf, 1997

root = expand_mutation_tree(root_cube, mutation_basis, n_layers, verbose=verbose)
