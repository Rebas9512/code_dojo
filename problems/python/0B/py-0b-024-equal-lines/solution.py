def equal_lines(grid: list[list[int]]) -> int:
    row_counts = {}
    for row in grid:
        key = tuple(row)
        row_counts[key] = row_counts.get(key, 0) + 1
    pairs = 0
    for c in range(len(grid)):
        column = []
        for row in grid:
            column.append(row[c])
        pairs += row_counts.get(tuple(column), 0)
    return pairs
