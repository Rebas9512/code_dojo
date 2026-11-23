def first_multiple(a: int, b: int, k: int) -> int:
    result = -1
    for x in range(a, b + 1):
        if x % k == 0:
            result = x
            break
    return result
