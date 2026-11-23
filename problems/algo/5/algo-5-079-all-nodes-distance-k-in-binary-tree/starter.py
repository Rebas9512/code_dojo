def distance_k(root: TreeNode, target: TreeNode, k: int) -> list[int]:
    pass


def run_case(root: TreeNode, value: int, k: int) -> list[int]:
    stack = [root]
    while stack:
        node = stack.pop()
        if node.val == value:
            return distance_k(root, node, k)
        stack.extend(c for c in (node.left, node.right) if c)
    return []
