def awards(rows: list[list]) -> list[list]:
    return sorted(rows, key=lambda row: (-row[1], row[0]))
