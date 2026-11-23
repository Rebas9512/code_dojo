def discount(price):
    price = price - 2
    return price


def label(price):
    return discount(price) + 1


price = 8
print(label(price))
print(price)
