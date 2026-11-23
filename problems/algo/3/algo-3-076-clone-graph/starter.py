def clone(start: Node | None) -> Node | None:
    pass

class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = [] if neighbors is None else neighbors


def run_case(adjacency: list[list[int]]) -> list[list[int]]:
    originals = [Node(i + 1) for i in range(len(adjacency))]
    for node, row in zip(originals, adjacency):
        node.neighbors = [originals[i-1] for i in row]
    root = clone(originals[0] if originals else None)
    if not originals:
        return [] if root is None else None
    if root is None or root.val != 1:
        return None
    by_value = {}
    stack = [root]
    old_nodes = set(originals)
    while stack:
        node = stack.pop()
        if node in old_nodes or not 1 <= node.val <= len(originals):
            return None
        if node.val in by_value:
            if by_value[node.val] is not node:
                return None
            continue
        by_value[node.val] = node
        stack.extend(node.neighbors)
    if len(by_value) != len(originals):
        return None
    for i, node in enumerate(originals):
        if node.val != i+1 or node.neighbors != [originals[k-1] for k in adjacency[i]]:
            return None
    return [sorted(other.val for other in by_value[i+1].neighbors) for i in range(len(originals))]
