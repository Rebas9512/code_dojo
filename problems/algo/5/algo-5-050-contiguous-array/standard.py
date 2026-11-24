def balanced(bits: list[int]) -> int:
    first = {0: -1}
    score = best = 0
    for i, bit in enumerate(bits):
        score += 1 if bit else -1
        if score in first:
            best = max(best, i - first[score])
        else:
            first[score] = i
    return best
