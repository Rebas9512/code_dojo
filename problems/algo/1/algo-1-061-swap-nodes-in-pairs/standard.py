def swap_pairs(head: ListNode | None) -> ListNode | None:
    dummy = ListNode(0, head)
    before = dummy
    while before.next and before.next.next:
        first = before.next
        second = first.next
        first.next = second.next
        second.next = first
        before.next = second
        before = first
    return dummy.next


def run_case(head: ListNode | None) -> ListNode | None:
    k = 2
    original = []
    node = head
    while node:
        original.append((node, node.val))
        node = node.next
    result = swap_pairs(head)
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
