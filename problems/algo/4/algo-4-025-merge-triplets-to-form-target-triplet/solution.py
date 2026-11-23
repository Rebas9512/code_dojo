def make_target(triplets: list[list[int]], target: list[int]) -> bool:
    best = [0, 0, 0]
    for row in triplets:
        if all(row[i] <= target[i] for i in range(3)):
            for i in range(3):
                best[i] = max(best[i], row[i])
    return best == target
