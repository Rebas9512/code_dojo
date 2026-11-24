def count_good(root: TreeNode) -> int:
    def visit(node, highest):
        if not node:
            return 0
        good = int(node.val >= highest)
        highest = max(highest, node.val)
        return good + visit(node.left, highest) + visit(node.right, highest)

    return visit(root, root.val)
