def pair_sums(a: list[int], b: list[int]) -> list[int]:
    result = []
    for x, y in zip(a, b):
        result.append(x + y)
    return result
