def max_profit(prices: list[int]) -> int:
    lowest = prices[0]
    profit = 0
    for price in prices:
        profit = max(profit, price - lowest)
        lowest = min(lowest, price)
    return profit
