def parse_int(text: str) -> int:
    i = 0
    while i < len(text) and text[i] == " ":
        i += 1
    sign = 1
    if i < len(text) and text[i] in "+-":
        sign = -1 if text[i] == "-" else 1
        i += 1
    value = 0
    bound = 2**31 if sign == -1 else 2**31 - 1
    while i < len(text) and "0" <= text[i] <= "9":
        value = min(bound, value * 10 + int(text[i]))
        i += 1
    return sign * value
