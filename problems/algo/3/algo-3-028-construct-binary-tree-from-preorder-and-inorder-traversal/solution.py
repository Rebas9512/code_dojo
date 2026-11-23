def restore(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    positions = {v: i for i, v in enumerate(inorder)}
    def build(start, low, high):
        if low >= high:
            return None
        value = preorder[start]
        mid = positions[value]
        left = build(start + 1, low, mid)
        right = build(start + 1 + mid - low, mid + 1, high)
        return TreeNode(value, left, right)
    return build(0, 0, len(inorder))
