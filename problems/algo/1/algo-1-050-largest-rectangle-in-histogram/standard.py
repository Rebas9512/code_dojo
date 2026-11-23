def largest_rectangle(heights: list[int]) -> int:
    stack = []
    best = 0
    for right, height in enumerate(heights + [0]):
        start = right
        while stack and stack[-1][1] > height:
            start, previous_height = stack.pop()
            best = max(best, previous_height * (right - start))
        stack.append((start, height))
    return best
