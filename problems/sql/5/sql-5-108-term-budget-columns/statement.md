## 题目

每个柜台 desk 的三个预算期 dawn、noon、dusk 各成一列。每个柜台每期至多登记一次；没登记输出 NULL，登记为 0 则输出 0。

## 样例输入

`term_grants`

| desk | term | coins |
|---|---|---|
| A | dawn | 20 |
| A | dusk | 0 |
| B | noon | 14 |

## 样例结果

| desk | dawn | noon | dusk |
|---|---|---|---|
| B | NULL | 14 | NULL |
| A | 20 | NULL | 0 |

A 的中期预算缺失，而晚期确实登记了 0。

按上表的列顺序输出。行序不限。
