## 题目

users 登记了读者姓名和电话。只返回 phone 缺失的读者，结果两列 user_id、name。

`users` 已经是 DataFrame。

## 示例 1

`users`

| user_id | name | phone |
| --- | --- | --- |
| 1 | Li Wei | 13800000001 |
| 2 | Zhang Min | 缺失 |
| 3 | Alice Brown | 15500000003 |

返回

| user_id | name |
| --- | --- |
| 2 | Zhang Min |

## 示例 2

`users`

| user_id | name | phone |
| --- | --- | --- |
| 5 | Bob Smith | 缺失 |
| 6 | Chen Jie | 18600000006 |
| 7 | Liu Yang | 13700000007 |

返回

| user_id | name |
| --- | --- |
| 5 | Bob Smith |

按示例的列名和列顺序返回。行的排列顺序可自选。行索引可自选。

同一道书店查询的 SQL 练习为 [sql-0-011-users-without-phone](/p/sql-0-011-users-without-phone)。
