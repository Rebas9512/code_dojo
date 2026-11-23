def ticket(n: int, price: int = 8) -> int:
    return n * price


def ticket_pair(n: int) -> list[int]:
    return [ticket(n), ticket(n, price=5)]
