def count_vowels(s: str) -> int:
    count = 0
    for ch in s:
        if ch in "aeiouAEIOU":
            count += 1
    return count
