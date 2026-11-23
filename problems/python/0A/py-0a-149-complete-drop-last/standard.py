def drop_last(items: list[str], k: int) -> list[str]:
    for i in range(k):
        if len(items) > 0:
            items.pop()
    return items
