def neighbor_ones(grid: list[list[int]]) -> list[list[int]]:
    if not grid:
        return []
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    result = []
    for row in range(rows):
        counts = []
        for col in range(cols):
            count = 0
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < rows and 0 <= c < cols:
                    count += grid[r][c]
            counts.append(count)
        result.append(counts)
    return result
