def add_words(a: int, b: int) -> int:
    mask = 0xffffffff
    a &= mask
    b &= mask
    while b:
        partial = (a ^ b) & mask
        carry = ((a & b) << 1) & mask
        a, b = partial, carry
    return a if a <= 0x7fffffff else ~(a ^ mask)
