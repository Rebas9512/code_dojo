def basket_total(prices: list[int], counts: list[int]) -> int:
    total = 0
    for i in range(len(prices)):
        total += prices[i] * counts[i]
    return total
