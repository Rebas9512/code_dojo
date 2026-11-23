## 题目

编辑器里是一条 MySQL 查询，在 PostgreSQL 上运行会报错。把它改写成 PostgreSQL 查询，让名册上的每位员工仍然得到原来的分机信息。

输出工号 `badge` 与分机号 `dial`。已分配的号码原样输出，没有号码时显示英文 `unrouted`。

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
