## 思路

每个窗口都有 k 个读数，和最大的窗口也有最大的平均值。先求第一个窗口的和，再让窗口每次右移一格，加上右边新进的读数，减去左边移出的读数。一路记下最大的和，最后除以 k。

## 复杂度

设有 n 个读数。第一个窗口累加 k 项，随后移动 n−k 次，时间 O(n)。只保留当前和、最大和以及下标，额外空间 O(1)。

## 写法要点

- 用第一个真实窗口的和初始化最大值。读数全为负时，初值 0 会让所有窗口都输给一个不存在的窗口。
- 相邻窗口重叠的 k−1 项无需重算。逐窗切片求和最多要做 O((n−k+1)k) 次工作。

## 进阶写法

`accumulate` 可以记录每个位置之前的总和，两项相减就是中间那段的和。若还要查询许多不同长度的区间，这张表可以反复用，代价是 O(n) 的额外空间。

```python
from itertools import accumulate


def max_average(nums: list[int], k: int) -> float:
    prefix = list(accumulate(nums, initial=0))
    return max(prefix[end] - prefix[end - k] for end in range(k, len(prefix))) / k
```
