## 题目

按名册输出 badge 与 dial。没有分机的员工显示 unrouted，已分配的号码原样输出。

原稿用的是 MySQL。编辑器里保留了原句的注释，下面的 PostgreSQL 译稿有一处意思译错了。

## 样例输入

`binders`

| badge | given | family |
|---|---|---|
| 11 | Ivo | Lane |
| 12 | Ona | Hall |
| 13 | Teo | Moss |

`extensions`

| badge | dial |
|---|---|
| 11 | X8 |
| 13 | X4 |

## 样例结果

| badge | dial |
|---|---|
| 11 | X8 |
| 13 | X4 |
| 12 | unrouted |

11 号已分到 X8；12 号才需要默认文字。

按上表的列顺序输出。行序不限。
