## 题目

order_counts 的每行是一个有过订单的读者及笔数 n。为 users 中每位读者返回 user_id、order_count，从未下单的读者填 0。

`users`、`order_counts` 已经是 DataFrame。

## 示例 1

`users`

| user_id | name |
| --- | --- |
| 1 | Li Wei |
| 2 | Zhang Min |
| 3 | Alice Brown |

`order_counts`

| user_id | n |
| --- | --- |
| 1 | 5 |
| 2 | 3 |
| 3 | 4 |

返回

| user_id | order_count |
| --- | --- |
| 1 | 5 |
| 2 | 3 |
| 3 | 4 |

## 示例 2

`users`

| user_id | name |
| --- | --- |
| 5 | Bob Smith |
| 6 | Chen Jie |
| 7 | Liu Yang |

`order_counts`

| user_id | n |
| --- | --- |

（空表）

返回

| user_id | order_count |
| --- | --- |
| 5 | 0 |
| 6 | 0 |
| 7 | 0 |

按示例的列名和列顺序返回。行的排列顺序可自选。行索引可自选。

同一道书店查询的 SQL 练习为 [sql-2-003-orders-for-every-reader](/p/sql-2-003-orders-for-every-reader)。
