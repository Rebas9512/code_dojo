def mirrored(text: str, left: int, right: int) -> bool:
    while left < right:
        if text[left] != text[right]:
            return False
        left += 1
        right -= 1
    return True


def almost_palindrome(text: str) -> bool:
    left, right = 0, len(text) - 1
    while left < right and text[left] == text[right]:
        left += 1
        right -= 1
    return mirrored(text, left + 1, right) or mirrored(text, left, right - 1)
