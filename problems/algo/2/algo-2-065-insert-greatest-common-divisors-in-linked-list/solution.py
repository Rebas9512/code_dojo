import math


def insert_gcd(head: ListNode) -> ListNode:
    node = head
    while node.next:
        following = node.next
        node.next = ListNode(math.gcd(node.val, following.val), following)
        node = following
    return head
