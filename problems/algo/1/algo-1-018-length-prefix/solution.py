def pack(words: list[str]) -> str:
    parts = []
    for word in words:
        parts.append(f"{len(word)}#{word}")
    return ''.join(parts)
