def median(a: list[int], b: list[int]) -> float:
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    half = (m + n + 1) // 2
    lo, hi = 0, m + 1
    while lo < hi:
        i = (lo + hi) // 2
        j = half - i
        if i < m and j > 0 and a[i] < b[j - 1]:
            lo = i + 1
        else:
            hi = i
    i, j = lo, half - lo
    left_a = a[i - 1] if i else float("-inf")
    left_b = b[j - 1] if j else float("-inf")
    lower = max(left_a, left_b)
    if (m + n) % 2:
        return lower
    right_a = a[i] if i < m else float("inf")
    right_b = b[j] if j < n else float("inf")
    return (lower + min(right_a, right_b)) / 2
