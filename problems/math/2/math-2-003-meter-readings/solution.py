def meter_table(units: list[int], base: int, rate: int) -> list[list[int]]:
    return [[x, base + rate * x] for x in units]
