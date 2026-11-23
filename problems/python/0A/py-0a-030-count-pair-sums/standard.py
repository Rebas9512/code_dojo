def count_pair_sums(n: int, target: int) -> int:
    count = 0
    for a in range(1, n + 1):
        for b in range(a + 1, n + 1):
            if a + b == target:
                count += 1
    return count
