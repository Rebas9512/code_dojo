def transpose(grid: list[list[int]]) -> list[list[int]]:
    if not grid:
        return []
    result = []
    for col in range(len(grid[0])):
        new_row = []
        for row in grid:
            new_row.append(row[col])
        result.append(new_row)
    return result
