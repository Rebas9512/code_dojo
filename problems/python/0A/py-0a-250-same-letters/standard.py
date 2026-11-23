def amounts(text: str) -> dict[str, int]:
    counts = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1
    return counts


def same_letters(a: str, b: str) -> bool:
    return amounts(a) == amounts(b)
