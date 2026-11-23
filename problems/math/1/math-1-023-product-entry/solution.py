def product_entry(a: list[list[int]], b: list[list[int]], r: int, c: int) -> int:
    total = 0
    for k in range(len(b)):
        total += a[r][k] * b[k][c]
    return total
