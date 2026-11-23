## 思路

先用 `prefix[i]` 存前 i 个数的和。固定左端点，让右端点从它开始向后走，每一段都用两个前缀和相减，结果为 k 就计一次。

## 复杂度

设有 n 个数，建表 O(n)，检查 n(n+1)/2 段，每段 O(1)，总时间 O(n²)，额外空间 O(n)。

## 写法要点

- 从 `right = left` 开始枚举，既会算到只有一个数的区间，又不会把空区间算进来。两次查表省去了反复累加重叠部分。

## 进阶写法

如果只要区间个数，可以记录每个前缀和已经出现过几次。当前前缀和减去 k 就是所需的旧前缀和，先查次数再登记当前值，平均 O(n) 时间、O(n) 额外空间就能数完。

```python
def count_target_ranges(nums: list[int], k: int) -> int:
    frequencies = {0: 1}
    prefix = 0
    count = 0
    for value in nums:
        prefix += value
        count += frequencies.get(prefix - k, 0)
        frequencies[prefix] = frequencies.get(prefix, 0) + 1
    return count
```
