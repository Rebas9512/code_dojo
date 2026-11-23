def reorder_list(head: ListNode) -> None:
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    current = slow.next
    slow.next = None
    back = None
    while current:
        following = current.next
        current.next = back
        back = current
        current = following
    front = head
    while back:
        following = front.next
        front.next = back
        back = back.next
        front.next.next = following
        front = following


def run_case(head: ListNode) -> ListNode:
    before = []
    node = head
    while node:
        before.append((node, node.val))
        node = node.next
    reorder_list(head)
    node = head
    for i in range(len(before)):
        index = i // 2 if i % 2 == 0 else len(before) - 1 - i // 2
        original, value = before[index]
        if node is not original or node.val != value:
            return None
        node = node.next
    return head if node is None else None
