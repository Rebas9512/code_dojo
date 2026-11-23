def visit(node, parents, seen, sequence):
    if node in seen:
        return
    seen.add(node)
    for parent in parents[node]:
        visit(parent, parents, seen, sequence)
    ...  # 补全这里


def order(parents, root):
    seen = set()
    sequence = []
    visit(root, parents, seen, sequence)
    return sequence
