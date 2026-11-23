from collections import defaultdict


def signature_groups(words: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for word in words:
        key = ____
        groups[key].append(word)
    return list(groups.values())
