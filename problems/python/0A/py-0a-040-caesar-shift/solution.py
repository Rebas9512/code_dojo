def caesar_shift(s: str, k: int) -> str:
    result = ""
    for ch in s:
        if "a" <= ch <= "z":
            index = (ord(ch) - ord("a") + k) % 26
            result += chr(ord("a") + index)
        else:
            result += ch
    return result
