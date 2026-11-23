def unlink_value(head: ListNode | None, x: int) -> ListNode | None:
    dummy = ListNode(0, head)
    previous = dummy
    while previous.next:
        if previous.next.val == x:
            previous.next = previous.next.next
        else:
            previous = previous.next
    return dummy.next
