def paths(root: TreeNode | None, target: int) -> list[list[int]]:
    result = []
    path = []

    def visit(node, left):
        if node is None:
            return
        path.append(node.val)
        left -= node.val
        if node.left is None and node.right is None and left == 0:
            result.append(path.copy())
        visit(node.left, left)
        visit(node.right, left)
        path.pop()

    visit(root, target)
    return result
