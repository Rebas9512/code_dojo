class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word: str) -> None:
        node = self.root
        for letter in word:
            node = node.setdefault(letter, {})
        node["#"] = True

    def _walk(self, text: str):
        node = self.root
        for letter in text:
            if letter not in node:
                return None
            node = node[letter]
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and "#" in node

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None
