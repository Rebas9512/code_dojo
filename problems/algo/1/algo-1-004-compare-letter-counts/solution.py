from collections import Counter


def count_gap(left: str, right: str, letter: str) -> int:
    return Counter(left)[letter] - Counter(right)[letter]
