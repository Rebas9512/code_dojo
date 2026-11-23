def water_rates(times: list[float], levels: list[float]) -> list[float]:
    out = []
    for i in range(1, len(times)):
        out.append((levels[i] - levels[i - 1]) / (times[i] - times[i - 1]))
    return out
