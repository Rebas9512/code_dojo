def successor(root: TreeNode, p: TreeNode) -> TreeNode | None:
    candidate = None
    while root:
        if root.val > p.val:
            candidate = root
            root = root.left
        else:
            root = root.right
    return candidate


def run_case(root: TreeNode, number: int) -> int | None:
    card = root
    while card.val != number:
        card = card.left if number < card.val else card.right
    result = successor(root, card)
    return result.val if result else None
