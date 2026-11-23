def shipping_fee(weight: int) -> int:
    if weight <= 1:
        return 10
    elif weight <= 5:
        return 15
    elif weight <= 20:
        return 30
    else:
        return 50
