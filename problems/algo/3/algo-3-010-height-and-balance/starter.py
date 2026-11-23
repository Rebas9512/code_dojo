def balance_info(root: TreeNode | None) -> tuple[int, bool]:
    if root is None:
        return 0, True
    left, left_ok = balance_info(root.left)
    right, right_ok = balance_info(root.right)
    return 1 + max(left, right), ____
