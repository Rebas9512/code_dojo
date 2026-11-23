def visit(node, values):
    if node is None:
        return
    visit(node.left, values)
    visit(node.right, values)
    values.append(node.val)


def traverse(root: TreeNode | None) -> list[int]:
    values = []
    visit(root, values)
    return values
