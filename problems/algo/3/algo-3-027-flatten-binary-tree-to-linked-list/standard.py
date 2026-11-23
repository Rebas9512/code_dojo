def flatten(root: TreeNode | None) -> None:
    node = root
    while node:
        if node.left:
            last = node.left
            while last.right:
                last = last.right
            last.right = node.right
            node.right = node.left
            node.left = None
        node = node.right


def run_case(root: TreeNode | None) -> list[int]:
    pending = [root] if root else []
    nodes = []
    while pending:
        node = pending.pop()
        nodes.append(node)
        if node.right:
            pending.append(node.right)
        if node.left:
            pending.append(node.left)
    flatten(root)
    values = []
    for original in nodes:
        if root is not original or root.left:
            return None
        values.append(root.val)
        root = root.right
    return values if root is None else None
