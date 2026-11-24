from collections import Counter


def min_cover(text: str, need: str) -> str:
    debt = Counter(need)
    missing = len(need)
    left = start = 0
    size = len(text) + 1
    for right, char in enumerate(text):
        if debt[char] > 0:
            missing -= 1
        debt[char] -= 1
        while missing == 0:
            if right - left + 1 < size:
                start, size = left, right - left + 1
            leaving = text[left]
            debt[leaving] += 1
            if debt[leaving] > 0:
                missing += 1
            left += 1
    return text[start : start + size] if size <= len(text) else ""
