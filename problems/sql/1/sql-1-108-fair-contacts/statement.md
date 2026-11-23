## 题目

每天每个展厅各出一行，依次返回 day、hall、不同来宾数 guests、不同代理人数 agents。

## 样例输入

`fair_notes`

| day | hall | guest | agent |
|---|---|---|---|
| 2025-05-01 | A | Kim | Fox |
| 2025-05-01 | A | Kim | Ray |
| 2025-05-01 | B | Kim | Fox |

## 样例结果

| day | hall | guests | agents |
|---|---|---|---|
| 2025-05-01 | A | 1 | 2 |
| 2025-05-01 | B | 1 | 1 |

A 厅当天两次接待 Kim，对应两名不同代理人。

按上表的列顺序输出。行序不限。
