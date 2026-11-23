def asteroid_collision(rocks: list[int]) -> list[int]:
    stack = []
    for rock in rocks:
        while stack and stack[-1] > 0 and rock < 0 and stack[-1] < -rock:
            stack.pop()
        if stack and stack[-1] > 0 and rock < 0:
            if stack[-1] == -rock:
                stack.pop()
        else:
            stack.append(rock)
    return stack
