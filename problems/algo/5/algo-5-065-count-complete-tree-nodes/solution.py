def count_nodes(root: TreeNode | None) -> int:
    left = right = root
    lh = rh = 0
    while left:
        lh += 1
        left = left.left
    while right:
        rh += 1
        right = right.right
    if lh == rh:
        return 2**lh - 1
    return 1 + count_nodes(root.left) + count_nodes(root.right)
