def row_sums(grid: list[list[int]]) -> list[int]:
    sums = []
    for row in grid:
        sums.append(sum(row))
    return sums
