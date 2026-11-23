def longest_uniform(text: str, k: int) -> int:
    counts = {}
    left = best = 0
    for right, ch in enumerate(text):
        counts[ch] = counts.get(ch, 0) + 1
        while right - left + 1 - max(counts.values()) > k:
            counts[text[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
