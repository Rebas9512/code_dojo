from collections import Counter


def starts(s: str, words: list[str]) -> list[int]:
    width = len(words[0])
    need = Counter(words)
    out = []
    for offset in range(width):
        have = Counter()
        left = offset
        size = 0
        for pos in range(offset, len(s) - width + 1, width):
            word = s[pos : pos + width]
            if word not in need:
                have.clear()
                size = 0
                left = pos + width
                continue
            have[word] += 1
            size += 1
            while have[word] > need[word]:
                have[s[left : left + width]] -= 1
                size -= 1
                left += width
            if size == len(words):
                out.append(left)
    return out
