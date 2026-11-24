from collections import Counter


def pal_length(text: str) -> int:
    pairs = sum(count // 2 * 2 for count in Counter(text).values())
    return pairs + (pairs < len(text))
