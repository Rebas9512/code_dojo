def visit(node, parents, seen, sequence):
    if node in seen:
        return
    seen.add(node)
    for parent in parents[node]:
        visit(parent, parents, seen, sequence)
    sequence.append(node)


def order(parents, root):
    seen = set()
    sequence = []
    visit(root, parents, seen, sequence)
    return sequence
