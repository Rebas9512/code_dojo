def min_gap(root: TreeNode) -> int:
    stack = []
    node = root
    last = None
    best = float("inf")
    while node or stack:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if last is not None:
            best = min(best, node.val - last)
        last = node.val
        node = node.right
    return best
