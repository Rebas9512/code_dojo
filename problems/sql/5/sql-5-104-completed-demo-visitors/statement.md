## 题目

列出至少一次完整走过试用、预订、付款的 visitor，每一步的 tick 都要严格晚于上一步，每人只列一次。

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

| visitor |
|---|
| A |

C 的付款没有晚于预订，不在名单中。A 的付款在预订之后。

按上表的列顺序输出。行序不限。
