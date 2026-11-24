def fewest(spans: list[list[int]]) -> int:
    point = None
    count = 0
    for a, b in sorted(spans, key=lambda span: span[1]):
        if point is None or a > point:
            point = b
            count += 1
    return count
