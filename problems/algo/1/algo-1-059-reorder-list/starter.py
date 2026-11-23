def reorder_list(head: ListNode) -> None:
    pass


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
