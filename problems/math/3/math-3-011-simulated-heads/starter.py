from random import seed, randint


def head_frequency(n: int, s: int) -> float:
    seed(s)
    heads = 0
    for i in range(n):
        heads += randint(0, 1)
    return ____
