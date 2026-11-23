def balanced(text: str) -> bool:
    depth = 0
    for char in text:
        if char == '(':
            depth += 1
        else:
            depth -= 1
        if depth < 0:
            return False
    return depth == 0
