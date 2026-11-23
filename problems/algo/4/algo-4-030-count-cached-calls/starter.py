from functools import cache


def fib_visits(n: int) -> list[int]:
    visits = 0

    @____
    def fib(i):
        nonlocal visits
        visits += 1
        if i < 2:
            return i
        return fib(i - 1) + fib(i - 2)

    value = fib(n)
    return [value, visits]
