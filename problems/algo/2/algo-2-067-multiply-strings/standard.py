def multiply(a: str, b: str) -> str:
    digits = [0] * (len(a) + len(b))
    for i in range(len(a) - 1, -1, -1):
        left_digit = int(a[i])
        for j in range(len(b) - 1, -1, -1):
            place = i + j + 1
            total = digits[place] + left_digit * int(b[j])
            digits[place] = total % 10
            digits[place - 1] += total // 10
    return "".join(str(d) for d in digits).lstrip("0") or "0"
