import numpy as np


def decode(nodes, i):
    flag, value = nodes[i]
    if flag == 0:
        return [int(value)], i + 1
    left, right_start = decode(nodes, i + 1)
    right, end = decode(nodes, right_start)
    return [value, left, right], end


def tree_predictions(nodes, queries):
    root, _ = decode(nodes, 0)
    result = []
    for x in queries:
        node = root
        while len(node) == 3:
            cut, left, right = node
            node = left if x <= cut else right
        result.append(node[0])
    return np.asarray(result, dtype=int)
