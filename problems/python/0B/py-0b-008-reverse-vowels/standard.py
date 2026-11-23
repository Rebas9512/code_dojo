def reverse_vowels(text: str) -> str:
    letters = list(text)
    vowels = "aeiouAEIOU"
    left, right = 0, len(letters) - 1
    while left < right:
        if letters[left] not in vowels:
            left += 1
        elif letters[right] not in vowels:
            right -= 1
        else:
            letters[left], letters[right] = letters[right], letters[left]
            left += 1
            right -= 1
    return "".join(letters)
