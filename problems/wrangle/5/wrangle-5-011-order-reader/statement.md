## 题目

orders 的每笔订单有 order_id、user_id，users 有读者编号 user_id 和姓名 name。按读者编号匹配，返回配对成功的 order_id、name。

`orders`、`users` 已经是 DataFrame。

## 示例 1

`orders`

| order_id | user_id |
| --- | --- |
| 101 | 1 |
| 102 | 2 |
| 103 | 1 |

`users`

| user_id | name |
| --- | --- |
| 1 | Li Wei |
| 2 | Zhang Min |
| 3 | Alice Brown |

返回

| order_id | name |
| --- | --- |
| 101 | Li Wei |
| 103 | Li Wei |
| 102 | Zhang Min |

## 示例 2

`orders`

| order_id | user_id |
| --- | --- |
| 105 | 4 |
| 106 | 5 |
| 107 | 1 |

`users`

| user_id | name |
| --- | --- |
| 5 | Bob Smith |
| 6 | Chen Jie |
| 7 | Liu Yang |

返回

| order_id | name |
| --- | --- |
| 106 | Bob Smith |

按示例的列名和列顺序返回。行的排列顺序可自选。行索引可自选。

同一道书店查询的 SQL 练习为 [sql-2-001-order-reader](/p/sql-2-001-order-reader)。
