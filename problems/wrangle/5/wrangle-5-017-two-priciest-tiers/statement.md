## 题目

没有定价的书不参评。每类保留最高两个不同价位上的所有书，同档并列全部保留。返回 book_id、category、price。

`shelf` 已经是 DataFrame。

## 示例 1

`shelf`

| book_id | category | price |
| --- | --- | --- |
| 71 | mini | 50.0 |
| 72 | mini | 50.0 |
| 73 | mini | 30.0 |
| 74 | mini | 20.0 |
| 75 | mini | 缺失 |

返回

| book_id | category | price |
| --- | --- | --- |
| 71 | mini | 50.0 |
| 72 | mini | 50.0 |
| 73 | mini | 30.0 |

## 示例 2

`shelf`

| book_id | category | price |
| --- | --- | --- |
| 1 | fiction | 42.0 |
| 2 | scifi | 39.0 |
| 8 | scifi | 45.0 |
| 22 | scifi | 39.0 |

返回

| book_id | category | price |
| --- | --- | --- |
| 1 | fiction | 42.0 |
| 8 | scifi | 45.0 |
| 2 | scifi | 39.0 |
| 22 | scifi | 39.0 |

按示例的列名和列顺序返回。行的排列顺序可自选。行索引可自选。

同一道书店查询的 SQL 练习为 [sql-4-005-two-priciest-tiers](/p/sql-4-005-two-priciest-tiers)。
