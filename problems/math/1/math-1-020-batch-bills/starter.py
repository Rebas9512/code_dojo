def batch_bills(orders: list[list[int]], prices: list[int]) -> list[int]:
    totals = []
    for row in orders:
        total = 0
        for i in range(len(prices)):
            total += ____
        totals.append(total)
    return totals
