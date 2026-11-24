def two_coasts(heights: list[list[int]]) -> list[list[int]]:
    rows, cols = len(heights), len(heights[0])

    def upstream(coast):
        reached = set(coast)
        stack = list(reached)
        while stack:
            row, col = stack.pop()
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = row + dr, col + dc
                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and heights[nr][nc] >= heights[row][col]
                    and (nr, nc) not in reached
                ):
                    reached.add((nr, nc))
                    stack.append((nr, nc))
        return reached

    top_left = [(0, col) for col in range(cols)] + [(row, 0) for row in range(rows)]
    bottom_right = [(rows - 1, col) for col in range(cols)] + [
        (row, cols - 1) for row in range(rows)
    ]
    both = upstream(top_left).intersection(upstream(bottom_right))
    return [list(cell) for cell in both]
