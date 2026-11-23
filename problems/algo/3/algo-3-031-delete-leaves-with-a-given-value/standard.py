def prune(root: TreeNode | None, target: int) -> TreeNode | None:
    if root:
        root.left = prune(root.left, target)
        root.right = prune(root.right, target)
        if root.val == target and not root.left and not root.right:
            return None
    return root
