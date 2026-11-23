def daily_temperatures(temperatures: list[int]) -> list[int]:
    wait = [0] * len(temperatures)
    pending = []
    for day, temp in enumerate(temperatures):
        while pending and temperatures[pending[-1]] < temp:
            old = pending.pop()
            wait[old] = day - old
        pending.append(day)
    return wait
