def mirrored(a, b):
    if not a or not b:
        return a is b
    return a.val == b.val and mirrored(a.left, b.right) and mirrored(a.right, b.left)


def symmetric(root: TreeNode | None) -> bool:
    return root is None or mirrored(root.left, root.right)
