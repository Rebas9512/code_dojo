def partition(head: ListNode | None, x: int) -> ListNode | None:
    small = left = ListNode()
    large = right = ListNode()
    while head:
        if head.val < x:
            left.next = head
            left = head
        else:
            right.next = head
            right = head
        head = head.next
    right.next = None
    left.next = large.next
    return small.next
