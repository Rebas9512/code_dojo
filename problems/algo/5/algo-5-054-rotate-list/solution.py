def rotate(head: ListNode | None, k: int) -> ListNode | None:
    if not head:
        return None
    tail = head
    length = 1
    while tail.next:
        tail = tail.next
        length += 1
    steps = k % length
    if not steps:
        return head
    cut = head
    for _ in range(length - steps - 1):
        cut = cut.next
    start = cut.next
    cut.next = None
    tail.next = head
    return start
