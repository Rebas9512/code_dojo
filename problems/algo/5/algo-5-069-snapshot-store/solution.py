class MemoryStore:
    def __init__(self):
        self.saved = {}
        self.records = {}
        self.now = 0

    def set(self, key: str, value: int) -> None:
        self.records[key] = (value, None)

    def get(self, key: str) -> int | None:
        if key not in self.records:
            return None
        value, end = self.records[key]
        if end is not None and self.now >= end:
            del self.records[key]
            return None
        return value

    def delete(self, key: str) -> bool:
        if self.get(key) is None:
            return False
        del self.records[key]
        return True

    def scan(self, prefix: str) -> list[str]:
        return sorted(
            key
            for key in list(self.records)
            if key.startswith(prefix) and self.get(key) is not None
        )

    def advance(self, now: int) -> None:
        self.now = now

    def set_ttl(self, key: str, value: int, ttl: int) -> None:
        self.records[key] = (value, self.now + ttl)

    def backup(self) -> None:
        self.saved = {}
        for key in list(self.records):
            value = self.get(key)
            if value is not None:
                end = self.records[key][1]
                self.saved[key] = (value, None if end is None else end - self.now)

    def restore(self) -> None:
        self.records = {}
        for key, (value, remaining) in self.saved.items():
            if remaining is None:
                self.set(key, value)
            else:
                self.set_ttl(key, value, remaining)
