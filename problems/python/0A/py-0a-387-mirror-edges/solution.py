def matches(text: str, lo: int, hi: int) -> bool:
    if lo >= hi:
        return True
    if text[lo] != text[hi]:
        return False
    return matches(text, lo + 1, hi - 1)


def mirror(text: str) -> bool:
    return matches(text, 0, len(text) - 1)
