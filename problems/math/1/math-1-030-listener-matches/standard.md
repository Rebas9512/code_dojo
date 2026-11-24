## 思路

固定一位听众，依次与每位听众比较。同一曲风的两个喜好分相乘，所有曲风的乘积之和就是这对听众的匹配分。

## 复杂度

有 n 位听众、d 种曲风，每对比较 d 项，时间 O(n²d)。结果占 O(n²) 空间，计算一格时只需常数额外空间。

## 写法要点

- 第二位听众的喜好已经是原表中的一行，直接读两行就能算点积，省去复制转置表。和自己配对时，同一写法自然得到各项的平方和。

## 进阶写法

交换两位听众，点积相同。如果听众很多，可以只算主对角线及其上方，把同一分数填入对称的两格，点积次数就从 n² 减到 n(n+1)/2。

```python
def listener_matches(tastes: list[list[int]]) -> list[list[int]]:
    count = len(tastes)
    scores = [[0] * count for _ in range(count)]
    for i, listener in enumerate(tastes):
        for j in range(i, count):
            score = sum(a * b for a, b in zip(listener, tastes[j]))
            scores[i][j] = score
            scores[j][i] = score
    return scores
```
