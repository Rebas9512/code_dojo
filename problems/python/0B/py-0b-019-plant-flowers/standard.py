def can_plant(bed: list[int], needed: int) -> bool:
    i = 0
    while needed > 0 and i < len(bed):
        left_free = i == 0 or bed[i - 1] == 0
        right_free = i == len(bed) - 1 or bed[i + 1] == 0
        if bed[i] == 0 and left_free and right_free:
            needed -= 1
            i += 2
        else:
            i += 1
    return needed == 0
