def common(a: list[int], b: list[int]) -> list[int]:
    remaining = set(b)
    result = []
    for value in a:
        if value in remaining:
            result.append(value)
            remaining.remove(value)
    return result
