def last_position(books: list[int], target: int) -> int:
    for i in range(len(books) - 1, -1, -1):
        if books[i] == target:
            return i
    return -1
