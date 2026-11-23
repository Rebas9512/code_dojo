class Cup:
    def __init__(self, level: int):
        self.level = level


def cup_levels(a: int, b: int, change: int) -> list[int]:
    first = Cup(a)
    second = Cup(b)
    second.level += change
    return [first.level, second.level]
