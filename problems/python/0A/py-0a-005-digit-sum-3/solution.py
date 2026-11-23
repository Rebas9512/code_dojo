def digit_sum_3(n: int) -> int:
    ones = n % 10
    tens = n // 10 % 10
    hundreds = n // 100
    return ones + tens + hundreds
