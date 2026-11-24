def supply_plan(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    result = []
    for order in a:
        amounts = []
        for ingredient in range(len(b[0])):
            amount = sum(order[meal] * b[meal][ingredient] for meal in range(len(order)))
            amounts.append(amount)
        result.append(amounts)
    return result
