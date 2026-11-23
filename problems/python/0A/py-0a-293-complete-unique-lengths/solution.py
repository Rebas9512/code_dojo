def length_kinds(words: list[str]) -> int:
    lengths = {len(word) for word in words}
    return len(lengths)
