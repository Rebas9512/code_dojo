## 题目

只要 ratings 中出现过一本书的 book_id，它就算有评分。返回从未被评过分的 book_id、title。书名可以重复。

`books`、`ratings` 已经是 DataFrame。

## 示例 1

`books`

| book_id | title |
| --- | --- |
| 1 | The Silent Harbor |
| 2 | Stars Over Gobi |
| 3 | Python in Practice |

`ratings`

| user_id | book_id | stars |
| --- | --- | --- |
| 3 | 1 | 4 |
| 4 | 2 | 4 |
| 5 | 2 | 5 |

返回

| book_id | title |
| --- | --- |
| 3 | Python in Practice |

## 示例 2

`books`

| book_id | title |
| --- | --- |
| 5 | The Last Lantern |
| 6 | Little Cloud |
| 7 | Noodles at Midnight |

`ratings`

| user_id | book_id | stars |
| --- | --- | --- |
| 1 | 3 | 5 |
| 10 | 3 | 4 |
| 16 | 3 | 5 |

返回

| book_id | title |
| --- | --- |
| 5 | The Last Lantern |
| 6 | Little Cloud |
| 7 | Noodles at Midnight |

按示例的列名和列顺序返回。行的排列顺序可自选。行索引可自选。

同一道书店查询的 SQL 练习为 [sql-2-006-unrated-books](/p/sql-2-006-unrated-books)。
