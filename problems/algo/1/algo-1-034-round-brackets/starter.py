def balanced(text: str) -> bool:
    depth = 0
    for char in text:
        if char == '(':
            depth += 1
        else:
            depth -= 1
    return depth == 0
