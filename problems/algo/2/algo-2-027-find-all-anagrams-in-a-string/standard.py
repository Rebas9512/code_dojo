from collections import Counter


def anagram_starts(text: str, pat: str) -> list[int]:
    width = len(pat)
    need = Counter(pat)
    window = Counter()
    starts = []
    for right in range(len(text)):
        window[text[right]] += 1
        if right >= width:
            window[text[right - width]] -= 1
        if window == need:
            starts.append(right + 1 - width)
    return starts
