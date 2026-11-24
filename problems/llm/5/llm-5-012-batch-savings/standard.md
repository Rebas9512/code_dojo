## 思路

一轮从长度 L 的前缀生成新词时，下一轮重新计算这个旧前缀会重复 1+2+…+L 个可见对。每个任务只累加这些本可复用的三角形，首轮两种方式工作相同。

## 复杂度

设有 J 个任务，第 j 个生成 Sⱼ 步。时间 O(J+ΣSⱼ)，额外空间 O(1)。

## 写法要点

- 直接数省下的旧查询，避免分别记录两份总数再相减。只有一步的任务没有旧前缀可复用。

## 进阶写法

长度从 1 到 n 的三角形加起来是 n(n+1)(n+2)/6，可以用两个这样的前缀和相减，直接算出一个任务重复的整段工作。设有 J 个任务，这样只用 O(J) 时间，即使某个任务生成很多步也只需算一次差。

```python
def triangle_sum(n):
    return n * (n + 1) * (n + 2) // 6


def batch_savings(jobs):
    saved = 0
    for prompt_len, steps in jobs:
        if steps > 1:
            last_repeated = prompt_len + steps - 2
            saved += triangle_sum(last_repeated) - triangle_sum(prompt_len - 1)
    return saved
```
