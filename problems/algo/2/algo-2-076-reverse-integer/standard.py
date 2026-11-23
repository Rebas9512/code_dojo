def reverse_int(x: int) -> int:
    negative = x < 0
    remaining = x if negative else -x
    result = 0
    last_allowed = 8 if negative else 7
    while remaining:
        # 在非正数范围内拆位，最小负数也无需取绝对值。
        digit = -(remaining % -10)
        remaining = -(remaining // -10)
        if result < -214748364 or (result == -214748364 and digit > last_allowed):
            return 0
        result = result * 10 - digit
    return result if negative else -result
