def tally(votes: list[str]) -> dict[str, int]:
    counts = {}
    for name in votes:
        counts[name] += 1
    return counts
