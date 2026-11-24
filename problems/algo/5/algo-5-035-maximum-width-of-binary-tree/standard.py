def width(root: TreeNode) -> int:
    level = [(root, 0)]
    best = 1
    while level:
        offset = level[0][1]
        best = max(best, level[-1][1] - offset + 1)
        children = []
        for node, index in level:
            pos = 2 * (index - offset)
            if node.left:
                children.append((node.left, pos))
            if node.right:
                children.append((node.right, pos + 1))
        level = children
    return best
