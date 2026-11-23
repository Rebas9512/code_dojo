def marked(points: list[list[int]]) -> int:
    seen = set()
    for row, col in points:
        seen.add((row, col))
    return len(seen)
