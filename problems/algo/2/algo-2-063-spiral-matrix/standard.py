def spiral(matrix: list[list[int]]) -> list[int]:
    top, bottom = 0, len(matrix)
    left, right = 0, len(matrix[0])
    result = []
    while top < bottom and left < right:
        for c in range(left, right):
            result.append(matrix[top][c])
        top += 1
        for r in range(top, bottom):
            result.append(matrix[r][right - 1])
        right -= 1
        if top < bottom:
            for c in range(right - 1, left - 1, -1):
                result.append(matrix[bottom - 1][c])
            bottom -= 1
        if left < right:
            for r in range(bottom - 1, top - 1, -1):
                result.append(matrix[r][left])
            left += 1
    return result
