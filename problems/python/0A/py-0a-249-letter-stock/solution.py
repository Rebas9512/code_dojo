def stamps(text: str) -> dict[str, int]:
    counts = {}
    for letter in text.lower():
        counts[letter] = counts.get(letter, 0) + 1
    return counts
