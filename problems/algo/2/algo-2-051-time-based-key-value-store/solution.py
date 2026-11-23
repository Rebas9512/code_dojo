class TimeMap:
    def __init__(self):
        self.history = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.history.setdefault(key, []).append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        records = self.history.get(key, [])
        lo, hi = 0, len(records)
        while lo < hi:
            mid = (lo + hi) // 2
            if records[mid][0] <= timestamp:
                lo = mid + 1
            else:
                hi = mid
        return records[lo - 1][1] if lo else ""
