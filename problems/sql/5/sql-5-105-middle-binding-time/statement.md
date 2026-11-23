## 题目

将每台机器的已知装订时长从小到大排好。输出 press、median_minutes；偶数个取中间两数的平均，全空组保留 NULL。

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

A 有效时长 2、4，中位数为 3；B 的 3、3、12 中，中间的是 3。

按上表的列顺序输出。行序不限。
