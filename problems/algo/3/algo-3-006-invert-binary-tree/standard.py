def invert(root: TreeNode | None) -> TreeNode | None:
    if root:
        root.left, root.right = invert(root.right), invert(root.left)
    return root
