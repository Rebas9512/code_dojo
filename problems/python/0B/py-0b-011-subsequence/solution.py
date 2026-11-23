def is_subsequence(word: str, text: str) -> bool:
    i = j = 0
    while i < len(word) and j < len(text):
        if word[i] == text[j]:
            i += 1
        j += 1
    return i == len(word)
