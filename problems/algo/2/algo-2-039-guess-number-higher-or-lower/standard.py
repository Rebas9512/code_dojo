def guess_number(n: int, guess) -> int:
    lo, hi = 1, n + 1
    while lo < hi:
        mid = (lo + hi) // 2
        if guess(mid) > 0:
            lo = mid + 1
        else:
            hi = mid
    return lo


class GuessTable:
    def __init__(self, pick: int):
        self._pick = pick

    def compare(self, value: int) -> int:
        if value < self._pick:
            return 1
        if value > self._pick:
            return -1
        return 0


def run_case(n: int, pick: int) -> int:
    return guess_number(n, GuessTable(pick).compare)
