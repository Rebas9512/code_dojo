def path_table(rows: int, cols: int) -> list[list[int]]:
    table = [[1] * cols for _ in range(rows)]
    for r in range(1, rows):
        for c in range(1, cols):
            table[r][c] = ____
    return table
