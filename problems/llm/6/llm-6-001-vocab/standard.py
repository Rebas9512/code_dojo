class CharVocab:
    def __init__(self, text):
        self.chars = sorted(set(text))
        self.ids = {char: i for i, char in enumerate(self.chars)}

    def encode(self, text):
        return [self.ids[char] for char in text]

    def decode(self, ids):
        return "".join(self.chars[i] for i in ids)
