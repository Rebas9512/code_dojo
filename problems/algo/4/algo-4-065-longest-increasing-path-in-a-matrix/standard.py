def rising_length(matrix: list[list[int]]) -> int:
    rows, cols = len(matrix), len(matrix[0])

    lengths = [[0] * cols for _ in range(rows)]

    def length(r, c):
        if lengths[r][c]:
            return lengths[r][c]
        best = 1
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and matrix[nr][nc] > matrix[r][c]):
                best = max(best, 1 + length(nr, nc))
        lengths[r][c] = best
        return best

    return max(length(r, c) for r in range(rows) for c in range(cols))
