def flatten(sticker_matrix):
    sticker_list = []
    for row in sticker_matrix:
        sticker_list.extend(row)
    return sticker_list


def N_and_flatten(sticker_matrix):
    N = len(sticker_matrix)
    return N, flatten(sticker_matrix)
