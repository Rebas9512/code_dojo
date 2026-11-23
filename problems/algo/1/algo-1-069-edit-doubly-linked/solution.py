def edit_list(head: ListNode | None, actions: list[list]) -> ListNode | None:
    dummy = ListNode(0, head)
    positions = {}
    before = dummy
    node = head
    while node:
        positions[node.val] = node
        node.prev = before
        before = node
        node = node.next
    for action, value in actions:
        if action == '加':
            node = ListNode(value, dummy.next)
            node.prev = dummy
            dummy.next = node
            positions[value] = node
        else:
            node = positions.pop(value)
            node.prev.next = node.next
        if node.next:
            if action == '加':
                node.next.prev = node
            else:
                node.next.prev = node.prev
    return dummy.next
