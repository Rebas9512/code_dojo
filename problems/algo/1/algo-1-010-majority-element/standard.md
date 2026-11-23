## 思路

统计每个编号的票数，再找得票严格超过半数的编号。题目保证有人达到这个门槛，找到即可返回。

## 复杂度

设有 n 张票、d 个不同编号，平均时间 O(n)，额外空间 O(d)。

## 写法要点

- 用总票数的一半作门槛，无需给候选人排序。严格大于也排除了恰好一半的情况。

## 进阶写法

若要把额外空间降到 O(1)，可以让两张不同的票互相抵消。过半者比其余选票合起来还多，最后留下的候选人必然就是它。

```python
def majority_element(nums: list[int]) -> int:
    candidate = nums[0]
    balance = 0
    for value in nums:
        if balance == 0:
            candidate = value
        if value == candidate:
            balance += 1
        else:
            balance -= 1
    return candidate
```
