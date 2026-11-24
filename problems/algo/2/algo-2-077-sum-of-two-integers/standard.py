def add_words(a: int, b: int) -> int:
    mask = 0xFFFFFFFF
    a &= mask
    b &= mask
    while b:
        partial = a ^ b
        carry = ((a & b) << 1) & mask
        a, b = partial, carry
    return a if a <= 0x7FFFFFFF else ~(a ^ mask)
