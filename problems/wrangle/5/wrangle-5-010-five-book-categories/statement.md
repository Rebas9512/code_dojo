## 题目

先按 category 数图书版本，再只保留至少有 5 个版本的类别。列名为 category、book_count。

`books` 已经是 DataFrame。

## 示例 1

`books`

| book_id | category |
| --- | --- |
| 2 | scifi |
| 8 | scifi |
| 15 | scifi |
| 22 | scifi |
| 28 | scifi |

返回

| category | book_count |
| --- | --- |
| scifi | 5 |

## 示例 2

`books`

| book_id | category |
| --- | --- |
| 5 | fantasy |
| 6 | kids |
| 7 | cooking |

返回

| category | book_count |
| --- | --- |

（空表）

按示例的列名和列顺序返回。行的排列顺序可自选。行索引可自选。

同一道书店查询的 SQL 练习为 [sql-1-004-five-book-categories](/p/sql-1-004-five-book-categories)。
