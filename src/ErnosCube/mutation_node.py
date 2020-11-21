class MutationNode:
    def __init__(self, parent, mutation, mut_seq):
        self.parent = parent
        self.mutation = mutation
        self.children = []

        if parent is None:
            assert mutation is None
            assert mut_seq is None
            self.mut_seq = []

        else:
            assert mutation is not None
            assert mut_seq is not None
            assert mut_seq[-1] == mutation
            self.mut_seq = mut_seq
            parent.children.append(self)

    def make_mut_seq(self, mutation):
        if self.parent is None:
            return [mutation]
        else:
            return [*self.mut_seq, mutation]
