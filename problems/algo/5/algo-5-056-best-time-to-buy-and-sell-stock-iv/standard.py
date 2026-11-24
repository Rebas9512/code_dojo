def profit(k: int, prices: list[int]) -> int:
    if k >= len(prices) // 2:
        return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))
    buy = [-prices[0]] * (k + 1)
    sell = [0] * (k + 1)
    for price in prices:
        for t in range(1, k + 1):
            buy[t] = max(buy[t], sell[t - 1] - price)
            sell[t] = max(sell[t], buy[t] + price)
    return sell[k]
