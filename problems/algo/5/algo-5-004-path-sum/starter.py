def has_path(root: TreeNode | None, target: int) -> bool:
    if root is None:
        return False
    remaining = target - root.val
    if remaining == 0 or (root.left is None and root.right is None):
        return remaining == 0
    return has_path(root.left, remaining) or has_path(root.right, remaining)
