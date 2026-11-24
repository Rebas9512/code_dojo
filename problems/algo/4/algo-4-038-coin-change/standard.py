def fewest_coins(coins: list[int], amount: int) -> int:
    missing = amount + 1
    best = [0] + [missing] * amount
    for total in range(1, amount + 1):
        for coin in coins:
            if coin <= total:
                best[total] = min(best[total], best[total - coin] + 1)
    return -1 if best[amount] == missing else best[amount]
