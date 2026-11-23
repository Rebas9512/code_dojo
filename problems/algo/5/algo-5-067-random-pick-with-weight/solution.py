from bisect import bisect_right
from random import Random, randrange, setstate


class WeightedPicker:
    def __init__(self, weights: list[int]):
        self.ends = []
        total = 0
        for weight in weights:
            total += weight
            self.ends.append(total)

    def pickIndex(self) -> int:
        ticket = randrange(self.ends[-1])
        return bisect_right(self.ends, ticket)


class PickTrial(WeightedPicker):
    def __init__(self, weights: list[int]):
        super().__init__(weights)
        self.weights = weights

    def sample(self, draws: int) -> bool:
        # 判题入口统计每个下标的抽中次数。
        setstate(Random(983).getstate())
        counts = [0] * len(self.weights)
        for _ in range(draws):
            index = self.pickIndex()
            if type(index) is not int or not 0 <= index < len(counts):
                return False
            counts[index] += 1
        total = sum(self.weights)
        for count, weight in zip(counts, self.weights):
            mean = draws * weight / total
            if abs(count - mean) > 8 * mean**0.5 + 8:
                return False
        return True
