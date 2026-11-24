def first_bad(n: int, is_bad) -> int:
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        if is_bad(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def run_case(n: int, first: int) -> int:
    def is_bad(version):
        return version >= first

    return first_bad(n, is_bad)
