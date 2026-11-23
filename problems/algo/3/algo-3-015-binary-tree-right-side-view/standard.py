from collections import deque


def right_view(root: TreeNode | None) -> list[int]:
    if root is None:
        return []
    queue = deque([root])
    visible = []
    while queue:
        visible.append(queue[-1].val)
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return visible
