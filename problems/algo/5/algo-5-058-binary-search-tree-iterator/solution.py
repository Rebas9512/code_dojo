class BSTIterator:
    def __init__(self, root: TreeNode):
        self.stack = []
        self._descend(root)

    def _descend(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        node = self.stack.pop()
        self._descend(node.right)
        return node.val

    def hasNext(self) -> bool:
        return bool(self.stack)


def run_case(root: TreeNode, calls: list[str]) -> list:
    it = BSTIterator(root)
    return [it.next() if op == "next" else it.hasNext() for op in calls]
