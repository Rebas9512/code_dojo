def recolor(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    old = image[sr][sc]
    if old == color:
        return image
    image[sr][sc] = color
    stack = [(sr, sc)]
    while stack:
        r, c = stack.pop()
        for i, j in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= i < len(image) and 0 <= j < len(image[0]) and image[i][j] == old:
                image[i][j] = color
                stack.append((i, j))
    return image
