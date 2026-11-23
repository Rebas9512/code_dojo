## 题目

books 每行是一个图书版本。交一张仅含 title 和 price 的清单，所有版本都要列出。补全起始代码中的 `____`。

`books` 已经是 DataFrame。

## 示例 1

`books`

| book_id | title | price |
| --- | --- | --- |
| 1 | The Silent Harbor | 42.0 |
| 2 | Stars Over Gobi | 39.0 |
| 3 | Python in Practice | 68.0 |

返回

| title | price |
| --- | --- |
| The Silent Harbor | 42.0 |
| Stars Over Gobi | 39.0 |
| Python in Practice | 68.0 |

## 示例 2

`books`

| book_id | title | price |
| --- | --- | --- |
| 5 | The Last Lantern | 39.0 |
| 6 | Little Cloud | 18.5 |
| 7 | Noodles at Midnight | 29.9 |

返回

| title | price |
| --- | --- |
| The Last Lantern | 39.0 |
| Little Cloud | 18.5 |
| Noodles at Midnight | 29.9 |

按示例的列名和列顺序返回。行的排列顺序可自选。行索引可自选。

同一道书店查询的 SQL 练习为 [sql-0-001-book-titles](/p/sql-0-001-book-titles)。
