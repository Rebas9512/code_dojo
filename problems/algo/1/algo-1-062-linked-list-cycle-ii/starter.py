def detect_cycle(head: ListNode | None) -> ListNode | None:
    pass


def run_case(head: ListNode | None, pos: int) -> int:

    nodes = []
    node = head
    while node:
        nodes.append(node)
        node = node.next
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    result = detect_cycle(head)
    if result is None:
        return -1
    for i, node in enumerate(nodes):
        if node is result:
            return i
    return -2
