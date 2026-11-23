def digit_counts(digits: list[int]) -> list[int]:
    counts = [0] * 10
    for d in digits:
        counts[d] += 1
    return counts
