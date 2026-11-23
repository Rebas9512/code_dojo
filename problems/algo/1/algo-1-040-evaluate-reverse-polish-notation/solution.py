def eval_rpn(tokens: list[str]) -> int:
    stack = []
    for token in tokens:
        if token not in ('+', '-', '*', '/'):
            stack.append(int(token))
            continue
        right = stack.pop()
        left = stack.pop()
        if token == '+':
            value = left + right
        elif token == '-':
            value = left - right
        elif token == '*':
            value = left * right
        else:
            value = int(left / right)
        stack.append(value)
    return stack.pop()
