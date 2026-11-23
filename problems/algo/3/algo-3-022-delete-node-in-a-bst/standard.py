def erase(root: TreeNode | None, key: int) -> TreeNode | None:
    if root is None:
        return None
    if key < root.val:
        root.left = erase(root.left, key)
    elif key > root.val:
        root.right = erase(root.right, key)
    elif not root.left:
        return root.right
    elif not root.right:
        return root.left
    else:
        successor = root.right
        while successor.left:
            successor = successor.left
        root.val = successor.val
        root.right = erase(root.right, successor.val)
    return root
