def is_valid(text: str) -> bool:
    pairs = {')': '(', ']': '[', '}': '{'}

    stack = []
    for char in text:
        if char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
        else:
            stack.append(char)
    return not stack
