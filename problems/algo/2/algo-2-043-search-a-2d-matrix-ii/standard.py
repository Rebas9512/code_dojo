def search_rows_cols(matrix: list[list[int]], target: int) -> bool:
    row, col = 0, len(matrix[0]) - 1
    while row < len(matrix) and col >= 0:
        value = matrix[row][col]
        if value == target:
            return True
        if value < target:
            row += 1
        else:
            col -= 1
    return False
