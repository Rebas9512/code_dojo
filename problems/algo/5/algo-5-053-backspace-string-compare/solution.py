def same_text(a: str, b: str) -> bool:
    def previous(text, i):
        skip = 0
        while i >= 0:
            if text[i] == "#":
                skip += 1
            elif skip:
                skip -= 1
            else:
                break
            i -= 1
        return i

    i, j = len(a) - 1, len(b) - 1
    while i >= 0 or j >= 0:
        i, j = previous(a, i), previous(b, j)
        if i < 0 or j < 0:
            return i == j
        if a[i] != b[j]:
            return False
        i -= 1
        j -= 1
    return True
