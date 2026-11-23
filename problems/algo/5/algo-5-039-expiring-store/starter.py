class MemoryStore:
    def __init__(self):
        self.records = {}

    def set(self, key: str, value: int) -> None:
        self.records[key] = value

    def get(self, key: str) -> int | None:
        return self.records.get(key)

    def delete(self, key: str) -> bool:
        return self.records.pop(key, None) is not None

    def scan(self, prefix: str) -> list[str]:
        return sorted(
            key
            for key in list(self.records)
            if key.startswith(prefix) and self.get(key) is not None
        )

    def advance(self, now: int) -> None:
        pass

    def set_ttl(self, key: str, value: int, ttl: int) -> None:
        pass
