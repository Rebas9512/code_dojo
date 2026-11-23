def reverse_between(head: ListNode, left: int, right: int) -> ListNode:
    dummy = ListNode(0, head)
    before = dummy
    for _ in range(left - 1):
        before = before.next
    tail = before.next
    for _ in range(right - left):
        moved = tail.next
        tail.next = moved.next
        moved.next = before.next
        before.next = moved
    return dummy.next
