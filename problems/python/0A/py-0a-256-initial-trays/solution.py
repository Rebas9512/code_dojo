def trays(words: list[str]) -> dict[str, list[str]]:
    groups = {}
    for word in words:
        key = word[0]
        if key not in groups:
            groups[key] = []
        groups[key].append(word)
    return groups
