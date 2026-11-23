def different_badges(a: list[int], b: list[int]) -> list[list[int]]:
    first = set(a)
    second = set(b)
    return [list(first - second), list(second - first)]
