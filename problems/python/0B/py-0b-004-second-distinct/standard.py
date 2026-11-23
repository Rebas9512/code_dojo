def second_highest(readings: list[int]) -> int | None:
    highest = second = None
    for value in readings:
        if highest is None or value > highest:
            second = highest
            highest = value
        elif value < highest and (second is None or value > second):
            second = value
    return second
