def evaluate(expr: str) -> int:
    stack = []
    total, sign, number = 0, 1, 0
    for ch in expr:
        if ch.isdigit():
            number = number * 10 + int(ch)
        elif ch in "+-":
            total += sign * number
            sign = 1 if ch == "+" else -1
            number = 0
        elif ch == "(":
            stack.append((total, sign))
            total, sign, number = 0, 1, 0
        elif ch == ")":
            inside = total + sign * number
            previous, factor = stack.pop()
            total = previous + factor * inside
            sign, number = 1, 0
    return total + sign * number
