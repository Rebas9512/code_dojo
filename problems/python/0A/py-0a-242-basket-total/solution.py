def checkout(prices: dict[str, int], basket: list[str]) -> int:
    total = 0
    for item in basket:
        total += prices[item]
    return total
