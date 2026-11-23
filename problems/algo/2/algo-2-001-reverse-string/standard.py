def reverse_string(chars: list[str]) -> None:
    left, right = 0, len(chars) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1


def run_case(chars: list[str]) -> list:
    reverse_string(chars)
    return chars
