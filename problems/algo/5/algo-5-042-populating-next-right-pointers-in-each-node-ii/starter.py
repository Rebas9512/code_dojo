def connect(root: TreeNode | None) -> TreeNode | None:
    pass


def run_case(root: TreeNode | None) -> list[list[int]]:
    # 平台的二叉节点只预置左右孩子，这里补上初始的空指针。
    todo = [root] if root else []
    while todo:
        node = todo.pop()
        node.next = None
        todo.extend(child for child in (node.left, node.right) if child)
    node = connect(root)
    rows = []
    seen = set()
    while node:
        row = []
        first = None
        while node:
            if node in seen:
                return []
            seen.add(node)
            row.append(node.val)
            first = first or node.left or node.right
            node = node.next
        rows.append(row)
        node = first
    return rows
