def within(node, low, high):
    if node is None:
        return True
    if not low < node.val < high:
        return False
    return within(node.left, low, node.val) and within(node.right, node.val, high)


def valid_bst(root: TreeNode | None) -> bool:
    return within(root, float('-inf'), float('inf'))
