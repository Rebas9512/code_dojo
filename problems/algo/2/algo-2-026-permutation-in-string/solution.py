from collections import Counter


def contains_permutation(pat: str, text: str) -> bool:
    if len(pat) > len(text):
        return False
    need = Counter(pat)
    window = Counter(text[:len(pat)])
    if window == need:
        return True
    for right in range(len(pat), len(text)):
        window[text[right - len(pat)]] -= 1
        window[text[right]] += 1
        if window == need:
            return True
    return False
