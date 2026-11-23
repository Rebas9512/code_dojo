def count_paths(root: TreeNode | None, target: int) -> int:
    counts = {0: 1}
    def walk(node, total):
        if not node:
            return 0
        total += node.val
        found = counts.get(total - target, 0)
        counts[total] = counts.get(total, 0) + 1
        found += walk(node.left, total) + walk(node.right, total)
        counts[total] -= 1
        return found
    return walk(root, 0)
