def find_mountain(target: int, mountain) -> int:
    pass


class MountainArray:
    def __init__(self, values: list[int]):
        self._values = values
        self._reads = 0

    def length(self) -> int:
        return len(self._values)

    def get(self, index: int) -> int:
        self._reads += 1
        assert self._reads <= 100, "读取超过 100 次"
        assert 0 <= index < self.length(), "下标越界"
        return self._values[index]


def run_case(target: int, values: list[int]) -> int:
    return find_mountain(target, MountainArray(values))
