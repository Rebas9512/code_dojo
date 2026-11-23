from collections import Counter


def group_runs(hand: list[int], size: int) -> bool:
    if len(hand) % size:
        return False
    counts = Counter(hand)
    for start in sorted(counts):
        copies = counts[start]
        if copies == 0:
            continue
        for value in range(start, start + size):
            if counts[value] < copies:
                return False
            counts[value] -= copies
    return True
