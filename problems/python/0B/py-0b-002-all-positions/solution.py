def all_positions(books: list[int], target: int) -> list[int]:
    positions = []
    for i, book in enumerate(books):
        if book == target:
            positions.append(i)
    return positions
