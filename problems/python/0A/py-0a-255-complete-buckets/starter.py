def by_size(words: list[str]) -> dict[str, list[str]]:
    groups = {}
    for word in words:
        key = str(len(word))
        if key not in groups:
            groups[key] = []
        ____
    return groups
