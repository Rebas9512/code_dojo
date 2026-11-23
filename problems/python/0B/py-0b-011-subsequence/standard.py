def is_subsequence(word: str, text: str) -> bool:
    matched = 0
    position = 0
    while matched < len(word) and position < len(text):
        if word[matched] == text[position]:
            matched += 1
        position += 1
    return matched == len(word)
