def remove_nth(head: ListNode, n: int) -> ListNode | None:
    dummy = ListNode(0, head)
    front = back = dummy
    for _ in range(n):
        front = front.next
    while front.next:
        front = front.next
        back = back.next
    back.next = back.next.next
    return dummy.next
