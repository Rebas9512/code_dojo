def has_cycle(head: ListNode | None) -> bool:
    pass


def run_case(head: ListNode | None, pos: int) -> bool:

    nodes = []
    node = head
    while node:
        nodes.append(node)
        node = node.next
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    return has_cycle(head)
