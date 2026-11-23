def balanced_height(node):
    if node is None:
        return 0
    left = balanced_height(node.left)
    if left == -1:
        return -1
    right = balanced_height(node.right)
    if right == -1 or abs(left - right) > 1:
        return -1
    return 1 + max(left, right)


def is_balanced(root: TreeNode | None) -> bool:
    return balanced_height(root) != -1
