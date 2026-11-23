def motion_rates(t: float, steps: list[float]) -> list[float]:
    base = t ** 3 + t
    rates = []
    for h in steps:
        after = (t + h) ** 3 + (t + h)
        rates.append((after - base) / h)
    return rates
