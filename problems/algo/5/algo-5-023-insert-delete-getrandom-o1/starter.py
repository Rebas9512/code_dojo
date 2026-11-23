from random import Random, randrange, setstate


class RandomizedSet:
    def __init__(self):
        pass

    def insert(self, val: int) -> bool:
        pass

    def remove(self, val: int) -> bool:
        pass

    def getRandom(self) -> int:
        pass


class SetTrial(RandomizedSet):
    def sample(self, members: list[int], draws: int) -> bool:
        # 固定标准库随机源的起点，允许不同算法消耗不同数量的随机数。
        setstate(Random(179).getstate())
        counts = {value: 0 for value in members}
        for _ in range(draws):
            value = self.getRandom()
            if type(value) is not int or value not in counts:
                return False
            counts[value] += 1
        mean = draws / len(members)
        return all(abs(count - mean) <= 8 * mean**0.5 for count in counts.values())
