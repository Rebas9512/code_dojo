def calculate(expr: str) -> int:
    total = term = number = 0
    op = "+"
    for i in range(len(expr) + 1):
        ch = expr[i] if i < len(expr) else "+"
        if ch.isdigit():
            number = number * 10 + int(ch)
        elif ch != " ":
            if op == "*":
                term *= number
            elif op == "/":
                sign = -1 if term < 0 else 1
                term = sign * (abs(term) // number)
            else:
                total += term
                term = number if op == "+" else -number
            number, op = 0, ch
    return total + term
