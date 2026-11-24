def rob(root: TreeNode | None) -> int:
    def choose(node):
        if not node:
            return 0, 0
        left_skip, left_take = choose(node.left)
        right_skip, right_take = choose(node.right)
        skip = max(left_skip, left_take) + max(right_skip, right_take)
        take = node.val + left_skip + right_skip
        return skip, take

    return max(choose(root))
