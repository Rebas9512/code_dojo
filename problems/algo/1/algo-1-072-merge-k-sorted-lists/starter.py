def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    pass


def run_case(chains: list[list[int]]) -> ListNode | None:
    heads = []
    for values in chains:
        dummy = tail = ListNode()
        for value in values:
            tail.next = ListNode(value)
            tail = tail.next
        heads.append(dummy.next)
    return merge_k_lists(heads)
