def two_coasts(heights: list[list[int]]) -> list[list[int]]:
    rows, cols = len(heights), len(heights[0])
    def inland(starts):
        seen = set(starts)
        stack = list(seen)
        while stack:
            r, c = stack.pop()
            for dr, dc in ((-1,0), (1,0), (0,-1), (0,1)):
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols and (nr,nc) not in seen
                        and heights[nr][nc] >= heights[r][c]):
                    seen.add((nr,nc))
                    stack.append((nr,nc))
        return seen
    first = inland([(0,c) for c in range(cols)] + [(r,0) for r in range(rows)])
    second = inland([(rows-1,c) for c in range(cols)] + [(r,cols-1) for r in range(rows)])
    return [list(cell) for cell in first.intersection(second)]
