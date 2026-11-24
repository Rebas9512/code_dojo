def build_tree(inorder: list[int], postorder: list[int]) -> TreeNode:
    position = {value: i for i, value in enumerate(inorder)}
    end = len(postorder) - 1

    def build(start, stop):
        nonlocal end
        if start == stop:
            return None
        root = TreeNode(postorder[end])
        end -= 1
        middle = position[root.val]
        root.right = build(middle + 1, stop)
        root.left = build(start, middle)
        return root

    return build(0, len(inorder))
