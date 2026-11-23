def rotate_image(matrix: list[list[int]]) -> None:
    size = len(matrix)
    for r in range(size):
        for c in range(r + 1, size):
            matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
    for row in matrix:
        row.reverse()


def run_case(matrix: list[list[int]]) -> list[list[int]]:
    rotate_image(matrix)
    return matrix
