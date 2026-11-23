## 题目

按 category 在本类内比较价格，价高的排在前，空价并列末位。返回 category、book_id、place、tier。place 用竞赛名次，tier 用连续档次。

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

| category | book_id | place | tier |
| --- | --- | --- | --- |
| mini | 71 | 1 | 1 |
| mini | 72 | 1 | 1 |
| mini | 73 | 3 | 2 |
| mini | 74 | 4 | 3 |
| mini | 75 | 5 | 4 |

## 示例 2

`shelf`

| book_id | category | price |
| --- | --- | --- |
| 1 | fiction | 42.0 |
| 2 | scifi | 39.0 |
| 8 | scifi | 45.0 |
| 22 | scifi | 39.0 |

返回

| category | book_id | place | tier |
| --- | --- | --- | --- |
| fiction | 1 | 1 | 1 |
| scifi | 8 | 1 | 1 |
| scifi | 2 | 2 | 2 |
| scifi | 22 | 2 | 2 |

按示例的列名和列顺序返回。行的排列顺序可自选。行索引可自选。

同一道书店查询的 SQL 练习为 [sql-4-004-two-price-ranks](/p/sql-4-004-two-price-ranks)。
