def unique_counts(records: list[int]) -> bool:
    counts = {}
    for badge in records:
        counts[badge] = counts.get(badge, 0) + 1
    frequencies = set(counts.values())
    return len(frequencies) == len(counts)
