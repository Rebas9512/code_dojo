def has_prefix(words: list[str], prefix: str) -> bool:
    root = {}
    for word in words:
        node = root
        for letter in word:
            node = ____
        node["#"] = True
    node = root
    for letter in prefix:
        if letter not in node:
            return False
        node = node[letter]
    return True
