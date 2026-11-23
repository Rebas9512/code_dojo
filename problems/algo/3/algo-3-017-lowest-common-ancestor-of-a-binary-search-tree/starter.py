def common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    pass

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
