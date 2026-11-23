def tally(votes: list[str]) -> dict[str, int]:
    counts = {}
    for name in votes:
        counts[name] = counts.get(name, 0) + 1
    return counts
