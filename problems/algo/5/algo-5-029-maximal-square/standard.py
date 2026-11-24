def max_square(matrix: list[list[str]]) -> int:
    prev = [0] * (len(matrix[0]) + 1)
    best = 0
    for row in matrix:
        current = [0] * len(prev)
        for j, value in enumerate(row, 1):
            if value == "1":
                current[j] = 1 + min(prev[j - 1], prev[j], current[j - 1])
                best = max(best, current[j])
        prev = current
    return best * best
