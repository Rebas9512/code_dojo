def daily_temperatures(temperatures: list[int]) -> list[int]:
    wait = [0] * len(temperatures)
    pending = []
    for day, temp in enumerate(temperatures):
        while pending and temperatures[pending[-1]] < temp:
            earlier_day = pending.pop()
            wait[earlier_day] = day - earlier_day
        pending.append(day)
    return wait
