from collections import Counter


def anagram_starts(text: str, pat: str) -> list[int]:
    if len(pat) > len(text):
        return []
    need = Counter(pat)
    window = Counter(text[:len(pat)])
    starts = [0] if window == need else []
    for right in range(len(pat), len(text)):
        window[text[right - len(pat)]] -= 1
        window[text[right]] += 1
        if window == need:
            starts.append(right - len(pat) + 1)
    return starts
