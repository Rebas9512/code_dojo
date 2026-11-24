def reverse_k_group(head: ListNode, k: int) -> ListNode:
    dummy = ListNode(0, head)
    before = dummy
    while before.next:
        end = before
        for _ in range(k):
            end = end.next
            if end is None:
                return dummy.next
        after = end.next
        previous = after
        current = before.next
        tail = current
        while current is not after:
            following = current.next
            current.next = previous
            previous = current
            current = following
        before.next = end
        before = tail
    return dummy.next


def run_case(head: ListNode, k: int) -> ListNode | None:
    original = []
    node = head
    while node:
        original.append((node, node.val))
        node = node.next
    result = reverse_k_group(head, k)
    node = result
    for start in range(0, len(original), k):
        block = original[start : start + k]
        if len(block) == k:
            block.reverse()
        for expected_node, value in block:
            if node is not expected_node or node.val != value:
                return ListNode("wrong node identity or value")
            node = node.next
    if node is not None:
        return ListNode("tail should point to None")
    return result
