def measure(node):
    if node is None:
        return 0, 0
    left, left_best = measure(node.left)
    right, right_best = measure(node.right)
    return 1 + max(left, right), max(left_best, right_best, left + right)


def diameter(root: TreeNode | None) -> int:
    return measure(root)[1]
