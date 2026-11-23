from collections import deque


def levels(root: TreeNode | None) -> list[list[int]]:
    if root is None:
        return []
    queue = deque([root])
    result = []
    while queue:
        layer = []
        for _ in range(____):
            node = queue.popleft()
            layer.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(layer)
    return result
