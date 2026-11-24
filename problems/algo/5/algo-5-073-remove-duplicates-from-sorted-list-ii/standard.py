def singles(head: ListNode | None) -> ListNode | None:
    dummy = ListNode(0, head)
    tail = dummy
    while head:
        first = head
        while head.next and head.next.val == first.val:
            head = head.next
        if first is head:
            tail = head
        else:
            tail.next = head.next
        head = head.next
    return dummy.next
