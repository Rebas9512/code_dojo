def can_plant(bed: list[int], needed: int) -> bool:
    planted = 0
    for i in range(len(bed)):
        left_free = i == 0 or bed[i - 1] == 0
        right_free = i == len(bed) - 1 or bed[i + 1] == 0
        if bed[i] == 0 and left_free and right_free:
            bed[i] = 1
            planted += 1
    return planted >= needed
