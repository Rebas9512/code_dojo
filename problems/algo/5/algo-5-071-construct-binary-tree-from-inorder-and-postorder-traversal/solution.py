def build_tree(inorder: list[int], postorder: list[int]) -> TreeNode:
    position = {value: i for i, value in enumerate(inorder)}

    def build(start, stop, end):
        if start >= stop:
            return None
        root = TreeNode(postorder[end])
        mid = position[root.val]
        right_size = stop - mid - 1
        root.left = build(start, mid, end - right_size - 1)
        root.right = build(mid + 1, stop, end - 1)
        return root

    return build(0, len(inorder), len(postorder) - 1)
