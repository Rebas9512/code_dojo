def calculate(expr: str) -> int:
    terms = []
    number = 0
    op = "+"
    for ch in expr + "+":
        if ch.isdigit():
            number = number * 10 + int(ch)
        elif ch != " ":
            if op == "+":
                terms.append(number)
            elif op == "-":
                terms.append(-number)
            elif op == "*":
                terms[-1] *= number
            else:
                sign = -1 if terms[-1] < 0 else 1
                terms[-1] = sign * (abs(terms[-1]) // number)
            number, op = 0, ch
    return sum(terms)
