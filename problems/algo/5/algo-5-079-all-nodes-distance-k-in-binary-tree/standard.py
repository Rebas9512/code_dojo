def distance_k(root: TreeNode, target: TreeNode, k: int) -> list[int]:
    parent = {root: None}
    stack = [root]
    while stack:
        node = stack.pop()
        for child in (node.left, node.right):
            if child:
                parent[child] = node
                stack.append(child)
    level = [target]
    seen = {target}
    for _ in range(k):
        following = []
        for node in level:
            for other in (node.left, node.right, parent[node]):
                if other and other not in seen:
                    seen.add(other)
                    following.append(other)
        level = following
        if not level:
            break
    return [node.val for node in level]


def run_case(root: TreeNode, value: int, k: int) -> list[int]:
    stack = [root]
    while stack:
        node = stack.pop()
        if node.val == value:
            return distance_k(root, node, k)
        stack.extend(c for c in (node.left, node.right) if c)
    return []
