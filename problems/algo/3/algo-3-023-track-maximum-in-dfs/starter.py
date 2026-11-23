def tree_max(root: TreeNode) -> int:
    best = root.val
    def visit(node):
        ____  # 让下面的赋值更新外层记录
        if node:
            best = max(best, node.val)
            visit(node.left)
            visit(node.right)
    visit(root)
    return best
