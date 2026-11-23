def price_of(prices: dict[str, int], item: str) -> int:
    return prices.get(item, 0)
