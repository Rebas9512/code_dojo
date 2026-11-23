## 题目

返回单行表，两列 users_total 与 with_phone 分别为全部读者数和电话非缺失的人数。即便输入为空也返回一行。补全起始代码中的 `____`。

`users` 已经是 DataFrame。

## 示例 1

`users`

| user_id | phone |
| --- | --- |
| 1 | 13800000001 |
| 2 | 缺失 |
| 3 | 15500000003 |

返回

| users_total | with_phone |
| --- | --- |
| 3 | 2 |

## 示例 2

`users`

| user_id | phone |
| --- | --- |
| 5 | 缺失 |
| 6 | 缺失 |
| 7 | 缺失 |

返回

| users_total | with_phone |
| --- | --- |
| 3 | 0 |

按示例的列名和列顺序返回。行的排列顺序可自选。行索引可自选。

同一道书店查询的 SQL 练习为 [sql-1-001-user-phone-counts](/p/sql-1-001-user-phone-counts)。
