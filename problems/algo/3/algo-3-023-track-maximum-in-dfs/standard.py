def tree_max(root: TreeNode) -> int:
    best = root.val
    def visit(node):
        nonlocal best
        if node:
            best = max(best, node.val)
            visit(node.left)
            visit(node.right)
    visit(root)
    return best
