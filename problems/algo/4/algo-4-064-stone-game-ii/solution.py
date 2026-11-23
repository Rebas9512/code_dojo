from functools import cache


def stone_limit(piles: list[int]) -> int:
    n = len(piles)
    suffix = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = piles[i] + suffix[i + 1]

    @cache
    def best(i, limit):
        if i + 2 * limit >= n:
            return suffix[i]
        return max(suffix[i] - best(i + take, max(take, limit))
                   for take in range(1, 2 * limit + 1))

    return best(0, 1)
