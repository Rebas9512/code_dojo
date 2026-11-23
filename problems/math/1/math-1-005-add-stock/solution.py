def add_stock(stock: list[int], delivery: list[int]) -> list[int]:
    return [stock[i] + delivery[i] for i in range(len(stock))]
