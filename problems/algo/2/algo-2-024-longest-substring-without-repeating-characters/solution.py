def longest_distinct(text: str) -> int:
    last = {}
    left = best = 0
    for right, char in enumerate(text):
        if char in last:
            left = max(left, last[char] + 1)
        best = max(best, right - left + 1)
        last[char] = right
    return best
