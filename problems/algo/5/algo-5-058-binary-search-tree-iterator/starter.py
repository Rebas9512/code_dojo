class BSTIterator:
    def __init__(self, root: TreeNode):
        pass

    def next(self) -> int:
        pass

    def hasNext(self) -> bool:
        pass


def run_case(root: TreeNode, calls: list[str]) -> list:
    it = BSTIterator(root)
    return [it.next() if op == "next" else it.hasNext() for op in calls]
