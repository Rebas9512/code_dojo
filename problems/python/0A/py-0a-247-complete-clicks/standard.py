def clicks(log: str) -> dict[str, int]:
    counts = {}
    for key in log:
        counts[key] = counts.get(key, 0) + 1
    return counts
