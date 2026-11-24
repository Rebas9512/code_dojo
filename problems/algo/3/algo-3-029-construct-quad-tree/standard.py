def construct(grid: list[list[int]]) -> Node:
    def build(row, col, size):
        if size == 1:
            return Node(bool(grid[row][col]), True)
        half = size // 2
        children = [build(row + dr, col + dc, half) for dr in (0, half) for dc in (0, half)]
        if all(child.isLeaf and child.val == children[0].val for child in children):
            return children[0]
        return Node(False, False, *children)

    return build(0, 0, len(grid))


class Node:
    def __init__(self, val, isLeaf, topLeft=None, topRight=None, bottomLeft=None, bottomRight=None):
        self.val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight


def run_case(grid: list[list[int]]) -> list:
    root = construct(grid)
    queue = [root]
    values = []
    for node in queue:
        if node is None:
            values.append(None)
            continue
        values.append([int(node.isLeaf), int(node.val)])
        queue.extend([node.topLeft, node.topRight, node.bottomLeft, node.bottomRight])
    while values and values[-1] is None:
        values.pop()
    return values
