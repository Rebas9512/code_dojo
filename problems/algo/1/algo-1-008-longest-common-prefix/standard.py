def longest_common_prefix(words: list[str]) -> str:
    first = words[0]
    for i, letter in enumerate(first):
        for index in range(1, len(words)):
            word = words[index]
            if i >= len(word) or word[i] != letter:
                return first[:i]
    return first
