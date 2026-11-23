def column_name(n: int) -> str:
    letters = []
    while n:
        n, digit = divmod(n - 1, 26)
        letters.append(chr(ord("A") + digit))
    return "".join(reversed(letters))
