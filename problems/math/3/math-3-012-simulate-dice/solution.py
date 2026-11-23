from random import seed, randint


def dice_frequency(n: int, s: int, threshold: int) -> float:
    seed(s)
    hits = 0
    for i in range(n):
        face = randint(1, 6)
        if face >= threshold:
            hits += 1
    return hits/n
