def palindrome_parts(s: str) -> list[list[str]]:
    result, parts = [], []

    def split(start):
        if start == len(s):
            result.append(parts[:])
            return
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word == word[::-1]:
                parts.append(word)
                split(end)
                parts.pop()

    split(0)
    return result
