def alarm(values: list[int], limit: int) -> bool:
    return any(x < limit for x in values)
