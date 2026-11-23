def guess_number(n: int, guess) -> int:
    pass


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
