def left_height(node):
    height = 0
    while node:
        height += 1
        node = node.left
    return height


def count_nodes(root: TreeNode | None) -> int:
    total = 0
    while root:
        left = left_height(root.left)
        right = left_height(root.right)
        if left == right:
            total += 2**left
            root = root.right
        else:
            total += 2**right
            root = root.left
    return total
