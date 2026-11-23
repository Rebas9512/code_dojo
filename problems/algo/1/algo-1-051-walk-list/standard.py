def describe_list(head: ListNode | None) -> list:
    values = []
    node = head
    while node is not None:
        values.append(node.val)
        node = node.next
    return [len(values), values]
