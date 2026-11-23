def runner_up(values: list[int]) -> int | None:
    levels = set(values)
    if len(levels) >= 2:
        levels.remove(max(levels))
        return max(levels)
    return None
