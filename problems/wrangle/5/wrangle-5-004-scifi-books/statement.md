## 题目

取 category 为 scifi 的所有图书，按 book_id、title 的列顺序返回。

`books` 已经是 DataFrame。

## 示例 1

`books`

| book_id | title | category |
| --- | --- | --- |
| 1 | The Silent Harbor | fiction |
| 2 | Stars Over Gobi | scifi |
| 3 | Python in Practice | programming |

返回

| book_id | title |
| --- | --- |
| 2 | Stars Over Gobi |

## 示例 2

`books`

| book_id | title | category |
| --- | --- | --- |
| 5 | The Last Lantern | fantasy |
| 6 | Little Cloud | kids |
| 7 | Noodles at Midnight | cooking |

返回

| book_id | title |
| --- | --- |

（空表）

按示例的列名和列顺序返回。行的排列顺序可自选。行索引可自选。

同一道书店查询的 SQL 练习为 [sql-0-003-scifi-books](/p/sql-0-003-scifi-books)。
