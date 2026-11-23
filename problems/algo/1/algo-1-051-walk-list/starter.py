def describe_list(head: ListNode | None) -> list:
    values = []
    node = head
    while node is not None:
        values.append(node.val)
        node = ____  # 沿箭头前进
    return [len(values), values]
