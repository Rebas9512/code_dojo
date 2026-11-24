class WordDictionary:
    def __init__(self):
        self.root = {}

    def addWord(self, word: str) -> None:
        node = self.root
        for letter in word:
            node = node.setdefault(letter, {})
        node["#"] = True

    def search(self, word: str) -> bool:
        def match(node, index):
            if index == len(word):
                return "#" in node
            letter = word[index]
            if letter == ".":
                for branch, child in node.items():
                    if branch != "#" and match(child, index + 1):
                        return True
                return False
            return letter in node and match(node[letter], index + 1)

        return match(self.root, 0)
