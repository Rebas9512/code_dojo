from collections import Counter


def contains_permutation(pat: str, text: str) -> bool:
    width = len(pat)
    need = Counter(pat)
    window = Counter()
    for right in range(len(text)):
        window[text[right]] += 1
        if right >= width:
            window[text[right - width]] -= 1
        if window == need:
            return True
    return False
