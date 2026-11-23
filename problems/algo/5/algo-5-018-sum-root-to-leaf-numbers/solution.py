def sum_numbers(root: TreeNode) -> int:
    def visit(node, prefix):
        if node is None:
            return 0
        current = prefix * 10 + node.val
        if not node.left and not node.right:
            return current
        return visit(node.left, current) + visit(node.right, current)

    return visit(root, 0)
