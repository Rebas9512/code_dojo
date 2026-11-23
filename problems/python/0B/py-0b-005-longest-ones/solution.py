def longest_ones(lights: list[int]) -> int:
    current = best = 0
    for light in lights:
        if light == 1:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best
