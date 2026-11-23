def net(entries: dict[str, int]) -> int:
    total = 0
    for amount in entries.values():
        total += amount
    return total
