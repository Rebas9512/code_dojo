def restore_rows(columns: list[list[int]]) -> list[list[int]]:
    rows = []
    for r in range(len(columns[0])):
        rows.append([column[r] for column in columns])
    return rows
