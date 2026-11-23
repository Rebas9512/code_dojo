def chain_total(head: ListNode | None) -> int:
    total = 0
    node = head
    while node is not None:
        total += node.val
        node = node.next
    return total
