## 题目

shelf 由书目取 book_id、category、price 得到。给每类书按价格从高到低编号，空价放最后，同价以小书号优先。返回 category、book_id、position，编号从 1 开始。补全起始代码中的 `____`。

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

| category | book_id | position |
| --- | --- | --- |
| mini | 71 | 1 |
| mini | 72 | 2 |
| mini | 73 | 3 |
| mini | 74 | 4 |
| mini | 75 | 5 |

## 示例 2

`shelf`

| book_id | category | price |
| --- | --- | --- |
| 1 | fiction | 42.0 |
| 2 | scifi | 39.0 |
| 8 | scifi | 45.0 |
| 22 | scifi | 39.0 |

返回

| category | book_id | position |
| --- | --- | --- |
| fiction | 1 | 1 |
| scifi | 8 | 1 |
| scifi | 2 | 2 |
| scifi | 22 | 3 |

按示例的列名和列顺序返回。行的排列顺序可自选。行索引可自选。

同一道书店查询的 SQL 练习为 [sql-4-003-category-row-numbers](/p/sql-4-003-category-row-numbers)。
