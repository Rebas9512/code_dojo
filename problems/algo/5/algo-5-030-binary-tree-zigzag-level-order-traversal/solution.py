def zigzag(root: TreeNode | None) -> list[list[int]]:
    level = [root] if root else []
    rows = []
    while level:
        values = [node.val for node in level]
        rows.append(values[::-1] if len(rows) % 2 else values)
        level = [c for node in level for c in (node.left, node.right) if c]
    return rows
