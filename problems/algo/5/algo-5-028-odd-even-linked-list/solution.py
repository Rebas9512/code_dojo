def regroup(head: ListNode | None) -> ListNode | None:
    if head is None:
        return None
    odd = head
    even = even_head = head.next
    while even and even.next:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next
        even = even.next
    odd.next = even_head
    return head
