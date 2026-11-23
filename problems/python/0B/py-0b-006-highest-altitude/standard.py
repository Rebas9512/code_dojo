def highest_altitude(changes: list[int]) -> int:
    altitude = peak = 0
    for change in changes:
        altitude += change
        peak = max(peak, altitude)
    return peak
