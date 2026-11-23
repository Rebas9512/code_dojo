def first_cold(readings: list[int]) -> int | None:
    for temperature in readings:
        if temperature < 0:
            return temperature
