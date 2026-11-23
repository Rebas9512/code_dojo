from collections import deque


def levels(root: TreeNode | None) -> list[list[int]]:
    if root is None:
        return []
    queue = deque([root])
    result = []
    while queue:
        layer = []
        for _ in range(len(queue)):
            node = queue.popleft()
            layer.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(layer)
    return result

def right_view(root: TreeNode | None) -> list[int]:
    return [layer[-1] for layer in levels(root)]
