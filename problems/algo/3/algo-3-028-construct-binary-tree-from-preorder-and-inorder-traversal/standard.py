def restore(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    positions = {value: index for index, value in enumerate(inorder)}
    next_root = 0

    def build(start, stop):
        nonlocal next_root
        if start == stop:
            return None
        value = preorder[next_root]
        next_root += 1
        middle = positions[value]
        left = build(start, middle)
        right = build(middle + 1, stop)
        return TreeNode(value, left, right)

    return build(0, len(inorder))
