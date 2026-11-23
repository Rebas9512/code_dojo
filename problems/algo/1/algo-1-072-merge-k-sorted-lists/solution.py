def merge_lists(a, b):
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            if i + 1 < len(lists):
                merged.append(merge_lists(lists[i], lists[i + 1]))
            else:
                merged.append(lists[i])
        lists = merged
    return lists[0] if lists else None


def run_case(chains: list[list[int]]) -> ListNode | None:
    heads = []
    for values in chains:
        dummy = tail = ListNode()
        for value in values:
            tail.next = ListNode(value)
            tail = tail.next
        heads.append(dummy.next)
    return merge_k_lists(heads)
