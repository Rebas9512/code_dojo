def scaled_move(start: list[int], end: list[int], factor: int) -> list[int]:
    return [(end[i] - start[i]) * factor for i in range(len(start))]
