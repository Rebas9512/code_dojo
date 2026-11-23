def stamps(text: str) -> dict[str, int]:
    counts = {}
    for letter in text:
        key = letter.lower()
        counts[key] = counts.get(key, 0) + 1
    return counts
