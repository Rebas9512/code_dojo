class Node:
    def __init__(self, val: int = 0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


def copy_random_list(head: Node | None) -> Node | None:
    copies = {None: None}
    node = head
    while node:
        copies[node] = Node(node.val)
        node = node.next
    node = head
    while node:
        copies[node].next = copies[node.next]
        copies[node].random = copies[node.random]
        node = node.next
    return copies[head]


def run_case(head: ListNode | None, targets: list[int | None]) -> list:
    originals = []
    node = head
    while node:
        originals.append(Node(node.val))
        node = node.next
    for i in range(1, len(originals)):
        originals[i - 1].next = originals[i]
    head = originals[0] if originals else None
    for i, target in enumerate(targets):
        originals[i].random = None if target is None else originals[target]
    original_set = set(originals)
    snapshot = [(n.val, n.next, n.random) for n in originals]
    node = copy_random_list(head)
    if snapshot != [(n.val, n.next, n.random) for n in originals]:
        return '原链被修改'
    copies = []
    positions = {}
    while node:
        if node in original_set or node in positions or len(copies) >= len(originals):
            return '副本混入了原节点或多余节点'
        positions[node] = len(copies)
        copies.append(node)
        node = node.next
    return [[n.val, positions.get(n.random, -1) if n.random else None] for n in copies]
