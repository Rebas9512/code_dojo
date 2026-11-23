def is_palindrome(n: int) -> bool:
    if n < 0 or (n and n % 10 == 0):
        return False
    half = 0
    while n > half:
        half = half * 10 + n % 10
        n //= 10
    return n == half or n == half // 10
