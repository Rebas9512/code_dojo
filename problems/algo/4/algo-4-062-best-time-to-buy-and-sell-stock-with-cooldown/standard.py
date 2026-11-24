def cooldown_profit(prices: list[int]) -> int:
    holding = -prices[0]
    sold = float("-inf")
    free = 0
    for i in range(1, len(prices)):
        price = prices[i]
        holding, sold, free = (max(holding, free - price), holding + price, max(free, sold))
    return max(sold, free)
