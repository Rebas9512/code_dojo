def is_vowel(ch: str) -> bool:
    return ch in "aeiouAEIOU"


def vowel_count(text: str) -> int:
    count = 0
    for ch in text:
        if is_vowel(ch):
            count += 1
    return count
