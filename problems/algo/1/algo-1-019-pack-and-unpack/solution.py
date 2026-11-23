class Codec:
    def encode(self, words: list[str]) -> str:
        parts = []
        for word in words:
            parts.append(f"{len(word)}#{word}")
        return ''.join(parts)

    def decode(self, packet: str) -> list[str]:
        words = []
        start = 0
        while start < len(packet):
            mark = packet.index('#', start)
            length = int(packet[start:mark])
            start = mark + 1
            words.append(packet[start:start + length])
            start += length
        return words
