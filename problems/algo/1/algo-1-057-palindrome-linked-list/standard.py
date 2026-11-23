def is_palindrome(head: ListNode | None) -> bool:
    values = []
    while head:
        values.append(head.val)
        head = head.next
    return values == values[::-1]
