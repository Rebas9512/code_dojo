def intersection(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    pass


def attach(head, shared):
    if not head:
        return shared
    tail = head
    while tail.next:
        tail = tail.next
    tail.next = shared
    return head


def run_case(a: ListNode | None, b: ListNode | None, shared: ListNode | None):
    a, b = attach(a, shared), attach(b, shared)
    links = {}
    for node in [a, b]:
        while node and node not in links:
            links[node] = node.next
            node = node.next
    result = intersection(a, b)
    if any(node.next is not following for node, following in links.items()):
        return '输入链的连接发生了变化'
    if result is not shared:
        return '返回的节点不是第一个共用节点'
    return result.val if result else None
