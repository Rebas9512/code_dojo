def same_shape(s: str, t: str) -> bool:
    forward = {}
    taken = set()
    for a, b in zip(s, t):
        if a in forward:
            if forward[a] != b:
                return False
        else:
            if b in taken:
                return False
            forward[a] = b
            taken.add(b)
    return True
