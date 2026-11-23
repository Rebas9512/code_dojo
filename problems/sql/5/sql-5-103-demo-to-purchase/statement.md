## 题目

按试用 sample → 预订 reserve → 付款 pay 的顺序计算三步各到达多少人。后一步的 tick 必须严格更大。输出一行 sampled、reserved、paid。

## 样例输入

`demo_steps`

| visitor | tick | action |
|---|---|---|
| A | 1 | sample |
| A | 3 | reserve |
| A | 5 | pay |
| B | 1 | pay |
| B | 2 | sample |
| B | 2 | reserve |
| C | 2 | sample |
| C | 4 | reserve |
| C | 4 | pay |

## 样例结果

| sampled | reserved | paid |
|---|---|---|
| 3 | 2 | 1 |

A 走完三步。C 在预订的同一时刻付款，因此只到第二步。

按上表的列顺序输出。行序不限。
