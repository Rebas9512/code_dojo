def averages(root: TreeNode) -> list[float]:
    level = [root]
    out = []
    while level:
        total = sum(node.val for node in level)
        out.append(total / len(level))
        level = [child for node in level for child in (node.left, node.right) if child]
    return out
