## 题目

为每个版本返回 book_id 和书名所含的字符数 chars。空格和标点都计一个字符。

`books` 已经是 DataFrame。

## 示例 1

`books`

| book_id | title |
| --- | --- |
| 1 | The Silent Harbor |
| 2 | Stars Over Gobi |
| 3 | Python in Practice |

返回

| book_id | chars |
| --- | --- |
| 1 | 17 |
| 2 | 15 |
| 3 | 18 |

## 示例 2

`books`

| book_id | title |
| --- | --- |
| 5 | The Last Lantern |
| 6 | Little Cloud |
| 7 | Noodles at Midnight |

返回

| book_id | chars |
| --- | --- |
| 5 | 16 |
| 6 | 12 |
| 7 | 19 |

按示例的列名和列顺序返回。行的排列顺序可自选。行索引可自选。

同一道书店查询的 SQL 练习为 [sql-0-150-complete-title-length](/p/sql-0-150-complete-title-length)。
