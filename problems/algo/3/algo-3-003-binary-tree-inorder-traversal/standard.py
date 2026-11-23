def visit(node, values):
    if node is None:
        return
    visit(node.left, values)
    values.append(node.val)
    visit(node.right, values)


def traverse(root: TreeNode | None) -> list[int]:
    values = []
    visit(root, values)
    return values
