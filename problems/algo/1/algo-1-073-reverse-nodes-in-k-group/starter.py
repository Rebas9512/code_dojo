def reverse_k_group(head: ListNode, k: int) -> ListNode:
    pass


def run_case(head: ListNode, k: int) -> ListNode | None:
    original = []
    node = head
    while node:
        original.append((node, node.val))
        node = node.next
    result = reverse_k_group(head, k)
    node = result
    for start in range(0, len(original), k):
        block = original[start:start + k]
        if len(block) == k:
            block.reverse()
        for expected_node, value in block:
            if node is not expected_node or node.val != value:
                return ListNode("节点身份或数值有误")
            node = node.next
    if node is not None:
        return ListNode("链尾应指向空")
    return result
