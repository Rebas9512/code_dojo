def depth(root: TreeNode | None) -> int:
    if not root:
        return 0
    return 1 + max(depth(root.left), depth(root.right))
