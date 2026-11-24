def sentences(s: str, words: list[str]) -> list[str]:
    dictionary = set(words)
    result, path, dead = [], [], set()

    def split(start):
        if start == len(s):
            result.append(' '.join(path))
            return True
        if start in dead:
            return False
        found = False
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in dictionary:
                path.append(word)
                if split(end):
                    found = True
                path.pop()
        if not found:
            dead.add(start)
        return found

    split(0)
    return result
