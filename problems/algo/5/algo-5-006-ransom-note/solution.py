from collections import Counter


def can_spell(note: str, source: str) -> bool:
    stock = Counter(source)
    for ch in note:
        if stock[ch] == 0:
            return False
        stock[ch] -= 1
    return True
