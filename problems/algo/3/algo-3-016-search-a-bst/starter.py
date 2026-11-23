def search(root: TreeNode | None, key: int) -> TreeNode | None:
    while root and root.val != key:
        if key < root.val:
            root = root.right
        else:
            root = root.right
    return root
