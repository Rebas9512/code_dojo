def runner_up(values: list[int]) -> int | None:
    levels = sorted(set(values))
    if len(levels) >= 2:
        return levels[-2]
    return None
