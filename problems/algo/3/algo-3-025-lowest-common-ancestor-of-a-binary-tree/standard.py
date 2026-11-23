def common_ancestor(root: TreeNode | None, p: TreeNode, q: TreeNode) -> TreeNode | None:
    if root is None or root is p or root is q:
        return root
    left = common_ancestor(root.left, p, q)
    right = common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left or right


def run_case(root: TreeNode, first: int, second: int) -> int:
    # 两个编号各自对应树中的一个现有节点。
    nodes = {}
    stack = [root]
    while stack:
        node = stack.pop()
        nodes[node.val] = node
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    ancestor = common_ancestor(root, nodes[first], nodes[second])
    if ancestor is not None and nodes.get(ancestor.val) is ancestor:
        return ancestor.val
    return None
