def water_rates(times: list[float], levels: list[float]) -> list[float]:
    rates = []
    for i in range(1, len(times)):
        rise = levels[i] - levels[i - 1]
        duration = times[i] - times[i - 1]
        rates.append(rise / duration)
    return rates
