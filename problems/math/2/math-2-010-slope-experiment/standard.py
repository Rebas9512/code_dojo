def motion_rates(t: float, steps: list[float]) -> list[float]:
    base = t**3 + t
    rates = []
    for h in steps:
        next_t = t + h
        after = next_t**3 + next_t
        rates.append((after - base) / h)
    return rates
