def orders(rows: list[list[str]]) -> dict[str, list[str]]:
    book = {}
    for guest, dish in rows:
        if guest not in book:
            book[guest] = []
        book[guest].append(dish)
    return book
