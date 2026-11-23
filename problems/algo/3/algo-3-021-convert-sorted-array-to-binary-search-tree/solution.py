def build(values, start, stop):
    if start >= stop:
        return None
    middle = (start + stop) // 2
    return TreeNode(values[middle], build(values, start, middle), build(values, middle + 1, stop))


def sorted_tree(values: list[int]) -> TreeNode | None:
    return build(values, 0, len(values))
