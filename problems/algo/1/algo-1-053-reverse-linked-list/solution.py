def reverse_list(head: ListNode | None) -> ListNode | None:
    previous = None
    current = head
    while current:
        following = current.next
        current.next = previous
        previous = current
        current = following
    return previous
