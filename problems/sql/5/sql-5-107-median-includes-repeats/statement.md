## 题目

输出每台印机的 press 与时长中位数 median_minutes。每条非空记录代表一次作业，即使时长相同也各占一个位置。全空组保留。

## 样例输入

`bind_times`

| press | minutes |
|---|---|
| A | 2 |
| A | 4 |
| A | NULL |
| B | 3 |
| B | 3 |
| B | 12 |
| C | NULL |

## 样例结果

| press | median_minutes |
|---|---|
| A | 3 |
| B | 3 |
| C | NULL |

B 的 3 分钟作业做过两次，它们在排好的三个值中占两个位置。

按上表的列顺序输出。行序不限。
