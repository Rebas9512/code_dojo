def visit(node, values):
    if node is None:
        return
    values.append(node.val)
    visit(node.left, values)
    visit(node.right, values)


def traverse(root: TreeNode | None) -> list[int]:
    values = []
    visit(root, values)
    return values
