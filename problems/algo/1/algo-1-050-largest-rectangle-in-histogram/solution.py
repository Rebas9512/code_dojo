def largest_rectangle(heights: list[int]) -> int:
    stack = []
    best = 0
    for i, height in enumerate(heights + [0]):
        start = i
        while stack and stack[-1][1] > height:
            start, old = stack.pop()
            best = max(best, old * (i - start))
        stack.append((start, height))
    return best
