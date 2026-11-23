def can_segment(s: str, words: list[str]) -> bool:
    dictionary = set(words)
    longest = max(len(word) for word in words)
    possible = [True] + [False] * len(s)
    for end in range(1, len(s) + 1):
        for start in range(max(0, end - longest), end):
            if possible[start] and s[start:end] in dictionary:
                possible[end] = True
                break
    return possible[-1]
