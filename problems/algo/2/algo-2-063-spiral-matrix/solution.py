def spiral(matrix: list[list[int]]) -> list[int]:
    top, bottom = 0, len(matrix)
    left, right = 0, len(matrix[0])
    result = []
    while top < bottom and left < right:
        result.extend(matrix[top][left:right])
        top += 1
        for r in range(top, bottom):
            result.append(matrix[r][right - 1])
        right -= 1
        if top < bottom:
            result.extend(reversed(matrix[bottom - 1][left:right]))
            bottom -= 1
        if left < right:
            for r in range(bottom - 1, top - 1, -1):
                result.append(matrix[r][left])
            left += 1
    return result
